import chromadb
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime

class CaptureAgent:
    """
    Agent 1: Capture Agent
    Role: Ingest any text input, generate embeddings, store in local ChromaDB.
    Data Firewall: All data stays local. Nothing sent to external APIs.
    """
    
    def __init__(self):
        # Local ChromaDB — data never leaves the device
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="second_brain",
            metadata={"hnsw:space": "cosine"}
        )
        # Open-source embedding model — runs locally, no API call
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def capture(self, text: str, category: str = "General") -> dict:
        """
        Capture a piece of knowledge.
        Steps: clean → embed → store in ChromaDB
        """
        # Clean the text
        clean_text = text.strip()
        
        # Generate embedding locally
        embedding = self.embedder.encode(clean_text).tolist()
        
        # Create unique ID
        memory_id = str(uuid.uuid4())[:8]
        
        # Store in local ChromaDB
        self.collection.add(
            documents=[clean_text],
            embeddings=[embedding],
            metadatas=[{
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "source": "user_input"
            }],
            ids=[memory_id]
        )
        
        return {
            "id": memory_id,
            "text": clean_text,
            "category": category,
            "status": "stored_locally"
        }
    
    def get_memory_count(self) -> int:
        return self.collection.count()
    
    def get_all_memories(self) -> list:
        if self.collection.count() == 0:
            return []
        results = self.collection.get()
        memories = []
        for i, doc in enumerate(results["documents"]):
            memories.append({
                "id": results["ids"][i],
                "text": doc,
                "category": results["metadatas"][i].get("category", "General")
            })
        return memories
    
    def clear_all(self):
        self.client.delete_collection("second_brain")
        self.collection = self.client.get_or_create_collection(
            name="second_brain",
            metadata={"hnsw:space": "cosine"}
        )
