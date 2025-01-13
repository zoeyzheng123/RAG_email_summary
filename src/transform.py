from bs4 import BeautifulSoup
from ollama import chat, ChatResponse
import re
from src.config import local_llm


local_llm = local_llm
def clean_content_with_ollama(content):
    if not content: return
    response: ChatResponse = chat(model=local_llm, messages=[
        {
            'role': 'user',
            'content': f"Please clean up this text by removing excessive special characters, disclaimers, and email signatures\n"
                       f"and clear up format to make it more readable"
                       f"do not need summarize the content: \nContent: {content}",
        },
    ])

    return response['message']['content']



def parse_content(content):
    if not content: return
    html_content = content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract plain text
    plain_text = soup.get_text()

    # Clean the text (remove extra whitespaces and control characters)
    cleaned_text = re.sub(r'\s+', ' ', plain_text).strip()
    return cleaned_text


def answer_question_with_ollama(vector_store, question, model=local_llm):
    """
    Use Ollama LLM to answer a question based on retrieved documents.
    """
    # Retrieve relevant documents
    retriever = vector_store.as_retriever(k=4)
    relevant_docs = retriever.invoke(question)

    if not relevant_docs:
        return "No relevant documents found to answer the question."

    # Combine the content of relevant documents into a context string
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Construct the prompt for the LLM
    prompt = (
        f"Based on the following documents, answer the question in detail:\n\n"
        f"{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    # Send the prompt to Ollama's LLM
    response = chat(model=model, messages=[{"role": "user", "content": prompt}])

    return response.get('message', {}).get('content', "No response from the model.")
