from vectorstore_manager import VectorStoreManager
from history_manager import HistoryManager
from chat_gemini import ChatGemini



class RAGPipeline:
    def __init__(self, session_id, pdf_files):
        self.vectorstore = VectorStoreManager().load_or_create_vectorstore(pdf_files)
        self.history = HistoryManager(session_id)
        self.llm = ChatGemini()



    def ask(self, query):
        docs = self.vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        chat_history = "\n".join([f"{h['role']}: {h['content']}" for h in self.history.load_history()])

        prompt = f"""
        You are a professional assistant that answers questions based on the user's uploaded PDF documents.

        Your primary goal:
        - Use the PDF context below to answer the user's question as accurately as possible.
        - If the answer is NOT found in the PDF, or is only partially related, say clearly:
        "The definition/details are not mentioned directly in the document, but based on related context from the file, here's what can be inferred."

        Rules:
        1. Always prioritize facts and examples found in the context.
        2. Never make up new document content — if it's not there, acknowledge it.
        3. You may provide a short general explanation only AFTER clarifying it's not in the document.
        4. Do NOT mention that you're an AI or language model.

        -----------------------
        📘 Document Context: {context}
        
        Chat history:
        {chat_history}

        Question: {query}
        """

        response = self.llm.get_response(prompt)
        self.history.save_turn("user", query)
        self.history.save_turn("assistant", response)
        return response
