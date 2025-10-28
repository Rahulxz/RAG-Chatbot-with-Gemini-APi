# 🤖 Smart RAG PDF Chatbot — Powered by Gemini LLM & Streamlit

**Project link:** https://rag-chatbot-with-gemini-api-projects.streamlit.app/

### _"Ask questions directly from your own PDFs — with AI that answers only from your documents."_

---

## 🧩 Overview

This project is an **intelligent document-based chatbot** built using **Streamlit** and the **Groq LLM API**.  
It allows users to **upload one or more PDF files**, and then **ask natural language questions** about the content.  
The chatbot retrieves relevant information from the PDFs and generates accurate answers in real time.

It combines **retrieval-augmented generation (RAG)** with a modern, responsive **ChatGPT-style interface** that includes:
- Session management  
- Persistent chat history  
- PDF ingestion and vector storage  
- Loading and status indicators  
- Clean, modern, customizable UI  

---

## 🚀 Key Features

✅ **Multi-PDF Uploading** — Upload and chat with multiple PDFs at once.  
✅ **Context-Aware Answers** — Model retrieves facts only from your uploaded files.  
✅ **Session Manager** — Create, rename, and switch between chat sessions seamlessly.  
✅ **Persistent Chat History** — Each session’s conversation is stored and automatically restored.  
✅ **Real-Time Loading Indicators** — Clear visual feedback while PDFs are processed or AI is generating.  
✅ **Modern UI** — ChatGPT-inspired interface with bright sidebar and fluid animations.  
✅ **Streamlit Deploy Support** — Deploy directly via Streamlit Cloud or custom server.  

---

## 🧠 Problem Statement

Reading and extracting information from large PDF documents is **slow and inefficient**.  
Traditional keyword search can’t understand context or relationships across sections.

---

## 💡 How This Project Solves It

This chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline:

1. **PDF Parsing**  
   Uploaded PDFs are read, text is extracted, and split into manageable text chunks.

2. **Vectorization & Indexing**  
   Each text chunk is embedded into numerical vectors using an embedding model.  
   These vectors are stored locally (e.g., in FAISS or ChromaDB).

3. **Query Understanding**  
   When you ask a question, your query is also vectorized.

4. **Context Retrieval**  
   The most relevant text chunks from your PDFs are retrieved based on vector similarity.

5. **Answer Generation (via Groq LLM)**  
   The retrieved context and your question are sent to the **Groq API**, which generates a contextualized answer.

6. **Response Display**  
   The answer appears in the chat interface, styled and color-coded with history stored per session.

This approach ensures:
- Factual accuracy (since answers are grounded in your PDFs)
- Efficiency (only relevant text is processed)
- Transparency (you control your documents and sessions)

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **LLM Backend** | Gemini LLM API |
| **Embeddings / Vector Search** | FAISS or ChromaDB |
| **Language** | Python 3.10+ |
| **Data Storage** | Local JSON (chat history), file-based index |
| **PDF Processing** | PyPDF2 / LangChain Document Loaders |

---

## 📂 Project Structure

