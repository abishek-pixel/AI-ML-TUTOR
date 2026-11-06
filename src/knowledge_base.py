"""Knowledge base with Sentence-BERT indexing and retrieval."""
import os
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from src.config import Config

class KnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer(Config.SENTENCE_TRANSFORMER_MODEL)
        self.index = None
        self.documents = []
        self.embeddings = None
    
    def load_and_index_notes(self, notes_path: str = None):
        """Load notes and create FAISS index."""
        if notes_path is None:
            notes_path = Config.NOTES_FILE
        
        # Load and parse documents
        with open(notes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into sections (by headers and paragraphs)
        self.documents = self._split_into_chunks(content)
        
        # Create embeddings
        self.embeddings = self.model.encode(self.documents, show_progress_bar=False)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))
        
        print(f"Indexed {len(self.documents)} document chunks")
    
    def _split_into_chunks(self, content: str) -> List[str]:
        """Split content into meaningful chunks."""
        chunks = []
        current_chunk = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
            elif line.startswith('#'):
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [line]
            else:
                current_chunk.append(line)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Filter out very short chunks
        return [chunk for chunk in chunks if len(chunk) > 50]
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search for relevant documents."""
        if self.index is None:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            top_k
        )
        
        # Convert L2 distance to similarity score (0-1)
        similarities = 1 / (1 + distances[0])
        
        results = []
        for idx, sim in zip(indices[0], similarities):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(sim)))
        
        return results
    
    def verify_answer(self, answer: str, query: str) -> Tuple[bool, List[str], float]:
        """Verify if answer is supported by knowledge base."""
        # Search for relevant documents
        results = self.search(query, top_k=5)
        
        if not results:
            return False, [], 0.0
        
        # Calculate average similarity
        avg_similarity = sum(sim for _, sim in results) / len(results)
        
        # Extract supporting documents
        supporting_docs = [doc for doc, sim in results if sim > Config.SIMILARITY_THRESHOLD]
        
        # Decision: answer is supported if we have relevant docs
        is_supported = avg_similarity > Config.SIMILARITY_THRESHOLD and len(supporting_docs) > 0
        
        return is_supported, supporting_docs, avg_similarity
    
    def save_index(self, path: str = None):
        """Save FAISS index to disk."""
        if path is None:
            path = Config.VECTOR_STORE_PATH
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(self.index, path)
    
    def load_index(self, path: str = None):
        """Load FAISS index from disk."""
        if path is None:
            path = Config.VECTOR_STORE_PATH
        
        if os.path.exists(path):
            self.index = faiss.read_index(path)
