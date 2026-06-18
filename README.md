# 🧠 Second Brain — AI-Powered Personal Knowledge System

> Built for the USAII Global AI Hackathon 2026 | Undergraduate Track

A three-agent AI system that captures, connects, and surfaces knowledge for the solo tech entrepreneur.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/second-brain-ai.git
cd second-brain-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Anthropic API key (optional — app works without it for capture/connect)
export ANTHROPIC_API_KEY=your_key_here

# 4. Run the app
streamlit run app.py
```

## 🏗️ Architecture

```
User Input
    ↓
Capture Agent  →  Embeds text locally (sentence-transformers)  →  ChromaDB (local)
    ↓
Connection Agent  →  Semantic search (cosine similarity)  →  Ranked memories
    ↓
Insight Agent  →  Anonymized prompt  →  Anthropic Claude API  →  Actionable insight
    ↓
User (approves before saving)
```

## 🛡️ Data Firewall

**Personal notes NEVER leave your device.**  
Only anonymized, summarized prompts are sent to the Anthropic API.  
ChromaDB runs entirely locally — no cloud sync, no third-party storage.

## 🧩 Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Orchestration | CrewAI |
| Vector Database | ChromaDB (local) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Primary LLM | Anthropic Claude claude-sonnet-4-6 |
| Frontend | Streamlit |
| Language | Python 3.11+ |

## 📋 Submission

- **Hackathon:** USAII Global AI Hackathon 2026
- **Track:** Undergraduate — "Build the Second Brain for Real Life"
- **Submitted by:** Dhruv Chopra
- **Deadline:** June 21, 2026

## ⚖️ Ethics

Built using Dr. Elizabeth Kohier's four-lens AI Ethics Framework:
- **Ethical:** Transparent outputs, user autonomy preserved
- **Legal:** GDPR-aligned, local data storage, right to deletion
- **Security:** Strict data firewall, no PII transmitted to APIs
- **Governance:** Human-in-the-loop, audit trail, override mechanism
