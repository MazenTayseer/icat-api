import os

import chromadb
from django.conf import settings


class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=os.path.join(settings.BASE_DIR, "chroma_db"))
        self.collection = self.client.get_or_create_collection("modules")

    def document_exists(self, document_id):
        return self.collection.get(ids=[f"doc_{document_id}"])

    def add_document(self, document):
        self.collection.add(
            documents=[document.text],
            metadatas=[{"document_id": document.id, "title": document.name}],
            ids=[f"doc_{document.id}"]
        )

    def search_documents(self, query_text, top_k=3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        doc_ids = [meta["document_id"] for meta in results["metadatas"][0]]
        return doc_ids
