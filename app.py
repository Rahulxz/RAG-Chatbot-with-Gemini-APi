import streamlit as st
from rag_pipeline import RAGPipeline
from session_manager import SessionManager
from history_manager import HistoryManager
import os
import time

# ------------------------------------------------------
# ⚙️ Streamlit Configuration
# ------------------------------------------------------
st.set_page_config(
    page_title="📚 Smart PDF Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------
# 🎨 UI Styling — Bright Sidebar, Visible Menu, Load Animations
# ------------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

.main {
    background: #ffffff;
    border-radius: 1rem;
    padding: 1.5rem 2.5rem;
    box-shadow: 0 4px 25px rgba(0,0,0,0.1);
}

.big-title {
    text-align: center;
    font-size: 2.3rem;
    color: #2563eb;
    font-weight: 800;
}
.sub-title {
    text-align: center;
    color: #334155;
    margin-bottom: 1.5rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eff6ff, #dbeafe);
    border-right: 2px solid #3b82f6;
}
.sidebar-header {
    font-size: 1.1rem;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.stSidebar, .stRadio > label, .stTextInput > label, .stFileUploader > label {
    color: #0f172a !important;
    font-weight: 600;
}

div.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.9);
    border: 1px dashed #2563eb;
    border-radius: 0.8rem;
    padding: 0.8rem;
    color: #1e3a8a !important;
}

.user-bubble {
    background: #3b82f6;
    color: white;
    padding: 0.9rem 1rem;
    border-radius: 1rem 1rem 0 1rem;
    margin: 0.4rem 0;
    text-align: right;
}
.bot-bubble {
    background: #f1f5f9;
    color: #0f172a;
    padding: 0.9rem 1rem;
    border-radius: 1rem 1rem 1rem 0;
    margin: 0.4rem 0;
}

/* Spinner Animation */
.loader {
  border: 4px solid rgba(0,0,0,0.1);
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  vertical-align: middle;
  margin-right: 8px;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}

/* Keep Streamlit top menu visible */
footer {visibility: visible;}
header {visibility: visible;}
#MainMenu {visibility: visible;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# 🧠 Initialize States
# ------------------------------------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager(st.session_state.sessions)

if "active_session" not in st.session_state:
    st.session_state.active_session = st.session_state.session_manager.create_session()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = st.session_state.sessions[st.session_state.active_session]

if "last_user_query" not in st.session_state:
    st.session_state.last_user_query = None

# ------------------------------------------------------
# 🧭 Sidebar: Session Management + File Upload
# ------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-header'>💬 Manage Conversations</div>", unsafe_allow_html=True)
sessions = list(st.session_state.sessions.keys())

if sessions:
    selected = st.sidebar.radio(
        "Active Session", sessions,
        index=sessions.index(st.session_state.active_session)
    )
    if selected != st.session_state.active_session:
        with st.spinner("🔄 Switching session..."):
            time.sleep(0.8)
        st.session_state.active_session = selected
        st.session_state.chat_history = st.session_state.sessions[selected]

# Rename session (always visible)
st.sidebar.markdown("#### ✏️ Rename This Session")
new_name = st.sidebar.text_input("Enter new session name", value=st.session_state.active_session)
if st.sidebar.button("Save Name"):
    with st.spinner("💾 Renaming session..."):
        time.sleep(0.8)
    renamed = st.session_state.session_manager.rename_session(st.session_state.active_session, new_name)
    st.session_state.active_session = renamed
    st.session_state.chat_history = st.session_state.sessions[renamed]
    st.sidebar.success(f"Renamed to: **{renamed}**")
    st.rerun()

# Create new chat
st.sidebar.markdown("---")
if st.sidebar.button("➕ New Chat", use_container_width=True):
    with st.spinner("✨ Creating new chat..."):
        time.sleep(0.8)
    new_session = st.session_state.session_manager.create_session()
    st.session_state.active_session = new_session
    st.session_state.chat_history = st.session_state.sessions[new_session]
    st.rerun()

# Upload PDFs
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='sidebar-header'>📄 Upload PDFs</div>", unsafe_allow_html=True)

uploaded_files = st.sidebar.file_uploader("Upload your documents", accept_multiple_files=True, type=["pdf"])
if uploaded_files:
    pdf_paths = []
    os.makedirs("data", exist_ok=True)
    with st.spinner("📚 Processing your PDFs... Please wait"):
        for file in uploaded_files:
            path = os.path.join("data", file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            pdf_paths.append(path)
        time.sleep(1.2)  # Simulate processing delay

    if "pipeline" not in st.session_state or st.session_state.pipeline is None:
        st.session_state.pipeline = RAGPipeline(st.session_state.active_session, pdf_paths)
        st.session_state.history_manager = HistoryManager(st.session_state.active_session)
        st.session_state.chat_history = st.session_state.history_manager.load_history()

# ------------------------------------------------------
# 🧾 Header
# ------------------------------------------------------
st.markdown("<div class='big-title'>🤖 RAG PDF Chatbot</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Chat with your uploaded PDFs — fully context-aware and session-based.</p>", unsafe_allow_html=True)

# ------------------------------------------------------
# 💬 Chat Window
# ------------------------------------------------------
if "pipeline" in st.session_state and st.session_state.pipeline:
    pipeline = st.session_state.pipeline
    history_manager = st.session_state.history_manager

    st.markdown(f"### 🗂️ Current Session: `{st.session_state.active_session}`")

    chat_col, _ = st.columns([3, 1])
    with chat_col:
        if len(st.session_state.chat_history) == 0:
            st.info("💬 Start chatting — ask any question from your uploaded PDFs.")
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"<div class='user-bubble'>🧑‍💻 {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

        # Chat input box
        user_input = st.chat_input("💭 Ask something from your documents...")

        if user_input:
            st.markdown(f"<div class='user-bubble'>🧑‍💻 {user_input}</div>", unsafe_allow_html=True)
            placeholder = st.empty()
            placeholder.markdown("<div class='bot-bubble'><span class='loader'></span> Generating answer...</div>", unsafe_allow_html=True)

            # Generate answer (show spinner)
            with st.spinner("🤖 Thinking..."):
                answer = pipeline.ask(user_input)
                time.sleep(0.5)

            placeholder.markdown(f"<div class='bot-bubble'>🤖 {answer}</div>", unsafe_allow_html=True)

            # Save history
            history_manager.save_turn("user", user_input)
            history_manager.save_turn("assistant", answer)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
else:
    st.warning("📥 Upload one or more PDFs in the sidebar to begin chatting.")

# ------------------------------------------------------
# 🧩 Footer
# ------------------------------------------------------
st.markdown("""
<hr style="border: 1px solid rgba(37,99,235,0.3); margin-top: 2rem;">
<p style="text-align:center; color:#1e3a8a;">
Built by <b>Rahul Mohapatra</b>
</p>
""", unsafe_allow_html=True)
