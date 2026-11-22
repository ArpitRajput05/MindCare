"""
MindCare RAG Engine & Vector Store Service
Handles document chunking, embedding generation, ChromaDB vector indexing, and semantic retrieval.
"""

import os
import glob
from typing import List, Dict, Any
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

from app.config import settings
from app.models.schemas import RetrievedSource


class RAGEngine:
    COLLECTION_NAME = "mindcare_wellness_kb"

    def __init__(self):
        self.kb_dir = Path(settings.KNOWLEDGE_BASE_DIR)
        self.chroma_dir = Path(settings.CHROMA_DIR)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB persistent client
        self.client = chromadb.PersistentClient(path=str(self.chroma_dir))

        # Default embedding function: ONNX all-MiniLM-L6-v2 (runs locally, free, no PyTorch needed)
        try:
            self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        except Exception:
            self.emb_fn = None

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self.emb_fn,
            metadata={"description": "MindCare Curated Student Wellbeing Knowledge Base"}
        )

        # Automatically index knowledge base if collection is empty
        self._ensure_indexed()

    def _parse_document(self, filepath: Path) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.strip().split("\n")
        metadata = {
            "title": "Wellness Guide",
            "source": "Health Authority",
            "category": "General",
            "filename": filepath.name
        }

        body_lines = []
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("Title:"):
                metadata["title"] = line_str.replace("Title:", "").strip()
            elif line_str.startswith("Source:"):
                metadata["source"] = line_str.replace("Source:", "").strip()
            elif line_str.startswith("Category:"):
                metadata["category"] = line_str.replace("Category:", "").strip()
            elif line_str:
                body_lines.append(line_str)

        body_text = " ".join(body_lines)
        return {"metadata": metadata, "text": body_text}

    def _chunk_text(self, text: str, max_chars: int = 500, overlap: int = 50) -> List[str]:
        # Split text into semantic chunks respecting sentence boundaries
        sentences = [s.strip() for s in text.replace(". ", ".\n").split("\n") if s.strip()]
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            if current_length + sentence_len > max_chars and current_chunk:
                chunks.append(" ".join(current_chunk))
                # Keep last sentence for overlap if short enough
                last_sentence = current_chunk[-1] if len(current_chunk[-1]) <= overlap else ""
                current_chunk = [last_sentence, sentence] if last_sentence else [sentence]
                current_length = sum(len(s) for s in current_chunk) + len(current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_len + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _ensure_indexed(self):
        doc_count = self.collection.count()
        if doc_count > 0:
            return

        doc_files = list(self.kb_dir.glob("*.txt"))
        if not doc_files:
            return

        ids = []
        documents = []
        metadatas = []

        for doc_path in doc_files:
            parsed = self._parse_document(doc_path)
            meta = parsed["metadata"]
            chunks = self._chunk_text(parsed["text"], max_chars=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)

            for idx, chunk in enumerate(chunks):
                chunk_id = f"{doc_path.stem}_chunk_{idx}"
                ids.append(chunk_id)
                documents.append(chunk)
                metadatas.append({
                    "title": meta["title"],
                    "source": meta["source"],
                    "category": meta["category"],
                    "filename": meta["filename"],
                    "chunk_index": idx
                })

        if documents:
            # Batch add to ChromaDB
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    def retrieve(self, query: str, top_k: int = 4) -> List[RetrievedSource]:
        """
        Retrieves top-k relevant knowledge base chunks for a student query or SHAP driver.
        """
        if not query.strip():
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, max(1, self.collection.count()))
        )

        retrieved: List[RetrievedSource] = []
        if not results or not results["documents"] or not results["documents"][0]:
            return retrieved

        docs = results["documents"][0]
        metas = results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)
        ids = results["ids"][0] if results["ids"] else [""] * len(docs)
        distances = results["distances"][0] if results.get("distances") and results["distances"] else [0.0] * len(docs)

        for doc_id, text, meta, dist in zip(ids, docs, metas, distances):
            # Chroma distances for cosine are 1 - cos_sim (or L2), convert to 0-1 relevance
            rel_score = round(max(0.0, 1.0 - (dist if dist is not None else 0.5)), 3)
            retrieved.append(RetrievedSource(
                doc_id=doc_id,
                title=meta.get("title", "Wellbeing Guide"),
                source=meta.get("source", "Health Guideline"),
                category=meta.get("category", "General"),
                snippet=text,
                relevance_score=rel_score
            ))

        return retrieved

    def retrieve_multi(self, queries: List[str], top_k_per_query: int = 2) -> List[RetrievedSource]:
        """
        Retrieves matching chunks across multiple queries (e.g. from multiple SHAP drivers),
        deduplicating by doc_id.
        """
        all_results: List[RetrievedSource] = []
        seen_ids = set()

        for q in queries:
            results = self.retrieve(q, top_k=top_k_per_query)
            for item in results:
                if item.doc_id not in seen_ids:
                    seen_ids.add(item.doc_id)
                    all_results.append(item)

        return all_results[:settings.TOP_K_CHUNKS]

    def format_sources_for_prompt(self, sources: List[RetrievedSource]) -> str:
        if not sources:
            return "No specific documents retrieved."

        formatted = []
        for i, s in enumerate(sources, 1):
            formatted.append(
                f"[Source {i}: {s.source} — {s.title} ({s.category})]\n{s.snippet}"
            )
        return "\n\n".join(formatted)


rag_engine = RAGEngine()
