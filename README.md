**Project Documentation: Smart PDF Chatbot (RAG System)**

Introduction

I developed the Smart PDF Chatbot to solve the common challenge of getting accurate, verifiable answers from proprietary documents. This system utilizes Retrieval-Augmented Generation (RAG) to ensure that every answer provided is strictly grounded in the content of the uploaded PDF files. My primary focus during development was to create a modular, performant, and reliable application capable of handling multiple documents while maintaining conversation history.

The entire application is built on Streamlit for a quick, interactive web interface, with the core logic separated into dedicated Python modules for clarity and maintainability.

1. Technologies and Libraries I Used My tech stack was carefully chosen to balance performance, functionality, and ease of deployment:

**Category**

Library : Technology

**Frontend**

streamlit : Frontend


The application framework for creating the user interface and managing session state.

**Large Language Model (LLM)**

google-genai / gemini-2.5-flash

The model I chose for fast, contextual, and accurate text generation.

**Vector Database**

FAISS (faiss-cpu)

Used for blazing-fast indexing and retrieval of text embeddings. Crucial for RAG performance.

**Embeddings**

HuggingFaceEmbeddings (MiniLM-L6-v2)

The model I used to transform document chunks into numerical vectors.

**Document Handling**

pypdf, langchain components

For loading raw PDF content and splitting it into optimal chunks.

**Environment**

python-dotenv

For securely loading my GEMINI_API_KEY from the hidden .env file.


**2. System Architecture and Modular Design**

I structured the project using a strict modular approach to keep components independent and reusable. This design allowed me to focus on one specific piece of logic per file.

**My Architecture Breakdown (Component Responsibilities)**

Module File

My Responsibility

Core Functions

**app.py**

The Orchestrator / UI Layer

Manages the Streamlit interface, handles user input, initializes all other services, and displays the final chat conversation.

**vectorstore_manager.py**

The Caching & Knowledge Base Engine

Handles document loading, text chunking, embedding generation, FAISS index creation, and, most importantly, caching to prevent re-processing documents unnecessarily.

**rag_pipeline.py**

The RAG Brain

Connects the vector store retrieval results with the LLM. It generates the final, comprehensive prompt that includes the current query, chat history, and the retrieved document chunks.

**chat_gemini.py**

The LLM Gateway

A thin wrapper around the Gemini API, responsible for securely loading the API key and sending the final prompt to the model to get a text response.

**history_manager.py**

Persistent History Storage

Manages saving and loading chat turns for a specific session ID to a persistent JSON file on the disk, ensuring history is available even after the app restarts.

**session_manager.py**

Active Session Management

Manages the creation, renaming, and retrieval of active session IDs and their temporary in-memory history using Streamlit's state.


**3. Deep Dive into Key Logic**

A. The Caching Strategy (vectorstore_manager.py)
To solve the performance problem of reprocessing large PDFs, I implemented a robust caching mechanism:

Metadata Check: My _has_pdf_changed function checks the modification time (os.path.getmtime) of every uploaded PDF.

Conditional Load: When the app starts, my load_or_create_vectorstore function first checks two things:

Does the FAISS cache file (kb_index.pkl) exist?

Have the source PDFs changed since the cache was created?

Instantaneous Startup: If the cache exists and the files are unchanged, I skip the entire RAG pipeline creation process and instantly deserialize the FAISS index using pickle.load. This dramatically improves the load time for returning users.

**B. The Retrieval-Augmented Generation (RAG) Process**

The magic happens in rag_pipeline.py within the ask(query) method:

Retrieval: I take the user's query and search my FAISS vector store, retrieving the top 3 most relevant docs. These are the snippets of text highly similar to the question.

Context Assembly: I assemble a single prompt that contains three critical components:

System Prompt/Rules: This sets strict behavioral guidelines for the LLM (e.g., "Use the PDF context below," "If not found, say clearly...").

Chat History: I pull the past turns from history_manager.py to give the LLM conversation context.

Document Context: I inject the raw text of the 3 retrieved document snippets directly into the prompt.

Grounded Generation: This final, comprehensive prompt is sent to the Gemini model. By including the context within the prompt, I force the model to ground its response in the provided text, achieving the required high-fidelity replication of document data.

**C. Conversation Persistence (history_manager.py)**

I ensured true data persistence across sessions (not just across Streamlit reruns).

Whenever a user completes a question-answer turn, the history_manager.save_turn() method is called.

This method appends the user query and the assistant's response to a dedicated JSON file named after the current session_id (chat_history/{session_id}.json).

This ensures that if the user closes and reopens the application, I can use the HistoryManager to reload the entire conversation, providing a seamless and continuous experience.
