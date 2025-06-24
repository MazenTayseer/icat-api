from setup import django_setup

django_setup()

import json
import re
from datetime import datetime

from apps.dal.models import Module
from common.clients.chroma_client import ChromaClient
from common.clients.gemini_client import GeminiClient


def calc_and_print_time(start_time, name):
    """Calculate and print the time taken for a process."""
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
    print(f"{name} time: {int(minutes)} minutes and {seconds:.2f} seconds.")


def __format_module_text(module_text: str, min_chunk_size: int = 150, max_chunk_size: int = 300) -> list[str]:
    """
    Format module text by:
    1. Parsing JSON data containing pages
    2. Excluding the references page (last page)
    3. Removing markdown formatting
    4. Creating larger chunks by combining pages
    5. Returning a list of cleaned text chunks
    """
    try:
        # Handle string representation of JSON
        if isinstance(module_text, str):
            pages_data = json.loads(module_text)
        else:
            pages_data = module_text

        # Exclude the last page (references) - but only if it's actually a references page
        content_pages = pages_data
        if len(pages_data) > 1:
            last_page = pages_data[-1].get('content', '').lower()
            if 'reference' in last_page or 'http' in last_page or 'accessed on' in last_page:
                content_pages = pages_data[:-1]  # Remove references page
                print("    🗂️  Excluded references page from processing")
            else:
                print(f"    📄 Processing all {len(pages_data)} pages (no references page detected)")

        # Clean all pages first
        cleaned_pages = []
        for page_data in content_pages:
            content = page_data.get('content', '')

            # Remove markdown formatting
            # Remove headers (# ## ###)
            content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

            # Remove bold/italic markers (**text** or *text*)
            content = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', content)

            # Remove inline code (`text`)
            content = re.sub(r'`([^`]+)`', r'\1', content)

            # Remove links [text](url)
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

            # Clean up extra whitespace and newlines
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = content.strip()

            if content:  # Only add non-empty content
                cleaned_pages.append(content)

        # Create larger chunks by combining pages
        formatted_chunks = []
        current_chunk = ""

        for page_content in cleaned_pages:
            # If adding this page would exceed max_chunk_size and we have content, start new chunk
            if current_chunk and len(current_chunk) + len(page_content) > max_chunk_size:
                formatted_chunks.append(current_chunk.strip())
                current_chunk = page_content
            else:
                # Add to current chunk with proper separation
                if current_chunk:
                    current_chunk += "\n\n" + page_content
                else:
                    current_chunk = page_content

        # Add the last chunk if it has content
        if current_chunk.strip():
            formatted_chunks.append(current_chunk.strip())

        # Post-process: ensure minimum chunk size by combining small chunks
        final_chunks = []
        i = 0
        while i < len(formatted_chunks):
            current = formatted_chunks[i]

            # If chunk is too small, try to combine with next chunks
            while (len(current) < min_chunk_size and i + 1 < len(formatted_chunks)):
                i += 1
                current += "\n\n" + formatted_chunks[i]

            final_chunks.append(current)
            i += 1

        print(f"    📦 Created {len(final_chunks)} larger chunks (avg size: {sum(len(c) for c in final_chunks) // len(final_chunks)} chars)")

        return final_chunks

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error processing module text: {e}")
        # Fallback: treat as plain text and return as single chunk
        return [module_text.strip()] if module_text else []


def process_modules_batch(modules, gemini_client, batch_size=10, min_chunk_size=150, max_chunk_size=300):
    """Process modules in batches to generate embeddings efficiently with configurable chunk sizes."""
    all_chunks = []
    all_embeddings = []
    all_metadata = []

    print(f"Processing {len(modules)} modules in batches of {batch_size}...")

    for i in range(0, len(modules), batch_size):
        batch_modules = modules[i:i + batch_size]
        batch_texts = []
        batch_metadata = []

        print(f"Processing batch {i//batch_size + 1}/{(len(modules)-1)//batch_size + 1}")

        # Format text chunks for each module in the batch
        for module in batch_modules:
            text_chunks = __format_module_text(module.text, min_chunk_size, max_chunk_size)

            for chunk_idx, chunk in enumerate(text_chunks):
                batch_texts.append(chunk)
                batch_metadata.append({
                    'module_id': module.id,
                    'module_name': module.name,
                    'chunk_index': chunk_idx,
                    'total_chunks': len(text_chunks)
                })

        # Generate embeddings for the batch
        if batch_texts:
            print(f"  Generating embeddings for {len(batch_texts)} chunks...")
            start_embed_time = datetime.now()

            # Generate embeddings for all texts in the batch
            batch_embeddings = []
            for idx, text in enumerate(batch_texts):
                metadata = batch_metadata[idx]
                print(f"    📄 Embedding chunk {idx + 1}/{len(batch_texts)}:")
                print(f"    🏷️  Module: {metadata['module_name']} (ID: {metadata['module_id']})")
                print(f"    📊 Chunk: {metadata['chunk_index'] + 1}/{metadata['total_chunks']}")
                print(f"    📏 Text length: {len(text)} characters")
                print(f"    📝 Preview: {text[:300]}...")
                if len(text) > 300:
                    print(f"    📝 ...and {len(text) - 300} more characters")
                print("-" * 60)

                embedding = gemini_client.embed(text)
                batch_embeddings.append(embedding)

            calc_and_print_time(start_embed_time, "  Batch embedding")

            # Add to overall collections
            all_chunks.extend(batch_texts)
            all_embeddings.extend(batch_embeddings)
            all_metadata.extend(batch_metadata)

    return all_chunks, all_embeddings, all_metadata


def create_collections_with_chroma_client(chroma_client: ChromaClient, chunks, embeddings, metadata, batch_size=1000):
    """Create ChromaDB collections us_ing the enhanced ChromaClient."""

    # --- Create main 'all_modules' collection ---
    print("\nCreating 'all_modules' collection...")
    try:
        chroma_client.delete_collection("all_modules")
        print("  Deleted existing 'all_modules' collection")
    except Exception as e:
        print(f"  No existing 'all_modules' collection to delete: {e}")

    all_modules_collection = chroma_client.create_collection("all_modules")

    # Prepare data for insertion
    ids = [f"chunk_{i}_{meta['module_id']}_{meta['chunk_index']}" for i, meta in enumerate(metadata)]

    # Add documents in batches using ChromaClient
    print(f"  Adding {len(chunks)} documents in batches of {batch_size}...")
    for i in range(0, len(chunks), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = embeddings[i:i + batch_size]
        batch_metadata = metadata[i:i + batch_size]

        all_modules_collection.add(
            documents=batch_chunks,
            ids=batch_ids,
            embeddings=batch_embeddings,
            metadatas=batch_metadata
        )
        print(f"    Added batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")

    print(f"  Created 'all_modules' collection with {len(chunks)} documents")

    # --- Create individual module collections ---
    print("\nCreating individual module collections...")

    # Group data by module
    module_groups = {}
    for i, meta in enumerate(metadata):
        module_id = meta['module_id']
        if module_id not in module_groups:
            module_groups[module_id] = {
                'chunks': [],
                'embeddings': [],
                'metadata': [],
                'ids': [],
                'name': meta['module_name']
            }

        module_groups[module_id]['chunks'].append(chunks[i])
        module_groups[module_id]['embeddings'].append(embeddings[i])
        module_groups[module_id]['metadata'].append(meta)
        module_groups[module_id]['ids'].append(ids[i])

    # Create collection for each module using ChromaClient
    for module_id, module_data in module_groups.items():
        collection_name = f"module_{module_id}"

        print(f"  Creating collection '{collection_name}' for module '{module_data['name']}'...")

        # Delete existing collection
        try:
            chroma_client.delete_collection(collection_name)
        except Exception:
            pass

        # Create new collection
        module_collection = chroma_client.create_collection(collection_name)

        # Add documents in batches
        module_chunks = module_data['chunks']
        for i in range(0, len(module_chunks), batch_size):
            batch_ids = module_data['ids'][i:i + batch_size]
            batch_chunks = module_data['chunks'][i:i + batch_size]
            batch_embeddings = module_data['embeddings'][i:i + batch_size]
            batch_metadata = module_data['metadata'][i:i + batch_size]

            module_collection.add(
                documents=batch_chunks,
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadata
            )

        print(f"    Created '{collection_name}' with {len(module_chunks)} documents")


if __name__ == "__main__":
    print("Starting ICAT ChromaDB embedding process...")
    start_total_time = datetime.now()

    # Initialize clients
    print("Initializing clients...")
    gemini_client = GeminiClient()
    chroma_client = ChromaClient()  # Use the enhanced ChromaClient

    # Load all modules from database
    print("Loading modules from database...")
    modules = list(Module.objects.all())  # type: ignore
    print(f"Found {len(modules)} modules to process")

    # Show detailed module information
    print("\n📚 Modules to be processed:")
    for i, module in enumerate(modules, 1):
        try:
            text_chunks = __format_module_text(module.text, 2000, 4000)
            print(f"  {i}. {module.name}")
            print(f"     📄 ID: {module.id}")
            print(f"     📊 Will create {len(text_chunks)} chunks")
        except Exception as e:
            print(f"  {i}. {module.name} - ⚠️  Error previewing: {e}")

    total_estimated_chunks = sum(len(__format_module_text(m.text, 2000, 4000)) for m in modules)
    print(f"\n🎯 Total estimated chunks to process: {total_estimated_chunks}")
    print("=" * 60)

    if not modules:
        print("No modules found in database. Exiting.")
        exit(1)

    # Process modules and generate embeddings
    print("\nProcessing modules and generating embeddings...")
    start_processing_time = datetime.now()

    all_chunks, all_embeddings, all_metadata = process_modules_batch(
        modules, gemini_client,
        batch_size=len(modules),  # Process all modules at once
        min_chunk_size=150,      # Minimum 2000 characters per chunk
        max_chunk_size=300       # Maximum 4000 characters per chunk
    )

    calc_and_print_time(start_processing_time, "Module processing and embedding")
    print(f"Generated {len(all_chunks)} total chunks from {len(modules)} modules")

    # Create ChromaDB collections using ChromaClient
    print("\nCreating ChromaDB collections...")
    start_collection_time = datetime.now()

    create_collections_with_chroma_client(chroma_client, all_chunks, all_embeddings, all_metadata)

    calc_and_print_time(start_collection_time, "Collection creation")

    # Print summary
    calc_and_print_time(start_total_time, "Total process")
    print(f"\n✅ Successfully processed {len(modules)} modules")
    print(f"✅ Created {len(all_chunks)} text chunks")
    print("✅ Generated embeddings and stored in ChromaDB")
    print(f"✅ Created {len(modules) + 1} collections (1 main + {len(modules)} individual)")
    print("\nCollections created:")
    print("  - all_modules (contains all chunks)")
    for module in modules:
        print(f"  - module_{module.id} ({module.name})")

    # Show collection statistics using ChromaClient
    print("\n📊 Collection Statistics:")
    try:
        collections = chroma_client.list_collections()
        for collection in collections:
            count = chroma_client.get_collection_stats(collection.name)
            print(f"  - {collection.name}: {count} documents")
    except Exception as e:
        print(f"  Error getting collection stats: {e}")
