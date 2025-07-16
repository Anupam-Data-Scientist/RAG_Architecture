import streamlit as st
from query_engine import search_and_respond
import re

# --- Streamlit Page Config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# --- Dark Mode Toggle ---
st.sidebar.markdown("### 🌗 Theme Settings")
dark_mode = st.sidebar.checkbox("Enable Dark Mode", value=False)

# Apply dark/light CSS
if dark_mode:
    st.markdown("""
        <style>
            body { background-color: #1e1e1e; color: #ffffff; }
            .main { background-color: #1e1e1e; padding: 2rem; }
            .stTextInput>div>div>input {
                background-color: #333333;
                color: #ffffff;
                border-radius: 10px;
            }
            .stButton>button {
                background-color: #009688;
                color: white;
            }
            .response-box {
                background-color: #2c2c2c;
                color: white;
                padding: 1rem;
                border-radius: 10px;
            }
            .context-box {
                font-size: 0.9rem;
                color: #bbbbbb;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .main {
                background-color: #f8f9fa;
                padding: 2rem;
            }
            .stTextInput>div>div>input {
                padding: 0.75rem;
                border-radius: 10px;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 0.5rem 1rem;
                font-size: 16px;
                border-radius: 8px;
            }
            .response-box {
                background-color: #ffffff;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.08);
            }
            .context-box {
                font-size: 0.9rem;
                color: #444;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=150)
    st.markdown("## 🚀 About this App")
    st.write("""
    This chatbot is built using:
    - FAISS for vector search
    - Sentence Transformers for embeddings
    - Gemini LLM (via Google API)

    You can:
    - Ask any question
    - Get responses grounded in documents
    - View document sources
    """)
    st.markdown("## 🔮 Future Enhancements")
    st.markdown("""
    - Chat history  
    - Upload custom PDFs  
    - Switch between LLMs  
    - Token cost monitoring  
    - Voice-to-text support
    """)

# --- Main Title ---
st.markdown("<h1 style='text-align: center;'>💬 RAG-Powered Q&A Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything and get responses backed by your documents</p>", unsafe_allow_html=True)

st.markdown("---")

# --- User Input ---
query = st.text_input("📌 Enter your question:", placeholder="e.g., What is a Large Language Model?")

# --- Submit ---
if st.button("Ask"):
    if not query.strip():
        st.warning("❗ Please enter a question.")
    else:
        with st.spinner("⚙️ Generating response..."):
            result = search_and_respond(query)

            def remove_citations(text):
                return re.sub(r"\[\d+\]", "", text).strip()

            if isinstance(result, dict):
                response = remove_citations(result["response"])
                st.markdown("### ✅ Response")
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

                # Show context (if available)
                if result.get("sources"):
                    with st.expander("📚 View Sources"):
                        for idx, chunk in enumerate(result["sources"], 1):
                            st.markdown(f"**[{idx}]** From `{chunk[1]}`")
                            st.markdown(f"<div class='context-box'>{chunk[0]}</div>", unsafe_allow_html=True)
            else:
                st.error(result)
