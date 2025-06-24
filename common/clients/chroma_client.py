import os

import chromadb
from django.conf import settings


class ChromaClient:
    def __init__(self, collection_name="all_modules"):
        self.client = chromadb.PersistentClient(path=os.path.join(settings.BASE_DIR, "chroma_db"))
        self.collection = self.client.get_or_create_collection(collection_name)

    def get_collection(self, collection_name):
        return self.client.get_collection(collection_name)

    def create_collection(self, collection_name):
        return self.client.create_collection(collection_name)

    def delete_collection(self, collection_name):
        return self.client.delete_collection(collection_name)

    def list_collections(self):
        return self.client.list_collections()

    def document_exists(self, document_id):
        return self.collection.get(ids=[f"doc_{document_id}"])

    def add_document(self, document_id, chunk, embedding):
        self.collection.add(
            documents=[chunk],
            metadatas=[{"document_id": document_id}],
            ids=[f"doc_{document_id}"],
            embeddings=[embedding] if embedding else None
        )

    def add_documents_batch(self, documents, ids, embeddings=None, metadatas=None):
        self.collection.add(
            documents=documents,
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search_documents(self, query_text, top_k=3, collection_name=None):
        if collection_name:
            collection = self.get_collection(collection_name)
        else:
            collection = self.collection

        results = collection.query(
            query_texts=[query_text],
            n_results=top_k
        )

        if results["metadatas"] and results["metadatas"][0]:
            doc_ids = [meta["document_id"] if "document_id" in meta else meta.get("module_id")
                      for meta in results["metadatas"][0]]
        else:
            doc_ids = []
        return doc_ids

    def search_with_embeddings(self, query_embedding, top_k=3, collection_name=None):
        if collection_name:
            collection = self.get_collection(collection_name)
        else:
            try:
                collection = self.get_collection("all_modules")
            except Exception:
                collection = self.collection

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def get_collection_stats(self, collection_name=None):
        if collection_name:
            collection = self.get_collection(collection_name)
        else:
            collection = self.collection

        return collection.count()
