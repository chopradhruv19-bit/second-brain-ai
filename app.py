import streamlit as st
import os
from agents.capture_agent import CaptureAgent
from agents.connection_agent import ConnectionAgent
from agents.insight_agent import InsightAgent

st.set_page_config(
    page_title="Second Brain - AI Knowledge System",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A5F, #2563EB);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .memory-card {
        background: #F3F4F6;
        border-left: 4px solid #2563EB;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .insight-card {
        background: #DCFCE7;
        border-left: 4px solid #166534;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .score-badge {
        background: #2563EB;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Second Brain</h1>
    <p>AI-Powered Personal Knowledge System for the Solo Tech Entrepreneur</p>
</div>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def load_agents():
    capture = CaptureAgent()
    connection = ConnectionAgent()
    insight = InsightAgent()
    return capture, connection, insight

capture_agent, connection_agent, insight_agent = load_agents()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    anthropic_key = st.text_input("Anthropic API Key", type="password", 
                                   value=os.environ.get("ANTHROPIC_API_KEY", ""))
    if anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    
    st.divider()
    st.markdown("### 🛡️ Data Firewall Status")
    st.success("✅ All data stored locally")
    st.info("ℹ️ Only anonymized prompts sent to LLM API")
    
    st.divider()
    st.markdown("### 📊 Knowledge Base Stats")
    try:
        count = capture_agent.get_memory_count()
        st.metric("Total Memories", count)
    except:
        st.metric("Total Memories", 0)
    
    st.divider()
    if st.button("🗑️ Clear All Memories", type="secondary"):
        if st.session_state.get("confirm_clear"):
            capture_agent.clear_all()
            st.success("Knowledge base cleared.")
            st.session_state["confirm_clear"] = False
        else:
            st.session_state["confirm_clear"] = True
            st.warning("Click again to confirm deletion.")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📥 Capture", "🔍 Connect & Insight", "📚 Knowledge Feed"])

# ─── TAB 1: CAPTURE ───
with tab1:
    st.markdown("### Add Knowledge to Your Second Brain")
    st.markdown("Paste notes, client feedback, ideas, research links, meeting takeaways — anything.")
    
    note_input = st.text_area(
        "What do you want to remember?",
        placeholder="e.g. Client XYZ wants minimalist design with warm tones. They loved the Figma draft. Follow up on Monday.",
        height=180
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        category = st.selectbox("Category", [
            "General", "Client Note", "Design", "Video", "Website", 
            "AI Agent", "Research", "Meeting", "Idea"
        ])
    
    if st.button("💾 Save to Second Brain", type="primary", use_container_width=True):
        if note_input.strip():
            with st.spinner("Capture Agent is processing your note..."):
                result = capture_agent.capture(note_input, category)
            st.success(f"✅ Memory saved! ID: `{result['id']}`")
            st.json({
                "Status": "Stored in local ChromaDB",
                "Category": category,
                "Characters": len(note_input),
                "Data Firewall": "Active — note never left your device"
            })
        else:
            st.warning("Please enter something to save.")

# ─── TAB 2: CONNECT & INSIGHT ───
with tab2:
    st.markdown("### Search Your Second Brain")
    
    query = st.text_input(
        "What are you working on?",
        placeholder="e.g. minimalist design for client website"
    )
    
    top_k = st.slider("Number of memories to retrieve", 1, 10, 5)
    
    if st.button("🔍 Find Related Memories", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Connection Agent is searching your knowledge base..."):
                results = connection_agent.search(query, top_k=top_k)
            
            if results:
                st.markdown(f"#### Found {len(results)} related memories:")
                
                for i, r in enumerate(results):
                    score = round(r.get("score", 0) * 100, 1)
                    st.markdown(f"""
                    <div class="memory-card">
                        <strong>#{i+1}</strong> &nbsp; <span class="score-badge">{score}% match</span>
                        &nbsp; <small>📁 {r.get('category', 'General')}</small>
                        <p style="margin-top:0.5rem">{r['text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                st.markdown("### 💡 Generate Insight")
                st.info("The Insight Agent will synthesize these memories into an actionable brief using Claude.")
                
                if st.button("✨ Generate Insight from Connected Memories", type="primary"):
                    if not os.environ.get("ANTHROPIC_API_KEY"):
                        st.error("Please add your Anthropic API key in the sidebar.")
                    else:
                        with st.spinner("Insight Agent is synthesizing your knowledge..."):
                            insight = insight_agent.generate_insight(query, results)
                        
                        st.markdown(f"""
                        <div class="insight-card">
                            <strong>🧠 Insight for: "{query}"</strong>
                            <p style="margin-top:0.5rem">{insight}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ Insight generated. Review above before using.")
            else:
                st.warning("No related memories found. Add some notes in the Capture tab first!")
        else:
            st.warning("Please enter a query.")

# ─── TAB 3: KNOWLEDGE FEED ───
with tab3:
    st.markdown("### 📚 All Stored Memories")
    
    if st.button("🔄 Refresh Feed"):
        st.rerun()
    
    try:
        all_memories = capture_agent.get_all_memories()
        if all_memories:
            for m in reversed(all_memories):
                with st.expander(f"📝 {m['text'][:80]}... | 📁 {m.get('category','General')}"):
                    st.write(m['text'])
                    st.caption(f"ID: {m['id']} | Category: {m.get('category','General')}")
        else:
            st.info("No memories yet. Start capturing in the Capture tab!")
    except Exception as e:
        st.info("No memories yet. Start capturing in the Capture tab!")
