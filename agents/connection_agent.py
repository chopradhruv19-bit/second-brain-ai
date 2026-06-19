import chromadb
from sentence_transformers import SentenceTransformer

class ConnectionAgent:
    """
    Agent 2: Connection Agent
    Role: Find semantically related memories using cosine similarity search.
    Data Firewall: All search happens locally in ChromaDB. No external API calls.
    """
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="second_brain",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def search(self, query: str, top_k: int = 5) -> list:
        """
        Semantic search: find memories most related to the query.
        Returns ranked list with similarity scores.
        """
        if self.collection.count() == 0:
            return []
        
        # Generate query embedding locally
        query_embedding = self.embedder.encode(query).tolist()
        
        # Search ChromaDB with cosine similarity
        n_results = min(top_k, self.collection.count())
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results with similarity scores
        memories = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                # Convert distance to similarity score (cosine: lower distance = higher similarity)
                distance = results["distances"][0][i]
                similarity = max(0, 1 - distance)
                
                memories.append({
                    "text": doc,
                    "score": similarity,
                    "category": results["metadatas"][0][i].get("category", "General"),
                    "id": results["ids"][0][i] if "ids" in results else str(i)
                })
        
        # Sort by score descending
        memories.sort(key=lambda x: x["score"], reverse=True)
        return memories
