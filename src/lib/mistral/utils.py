# IMPORT from Core libraries
import os
# IMPORT from External libraries
from mistralai import Mistral
# IMPORT from Internal libraries

# SET const variables
model='open-mistral-nemo'

# INSTANTIATE Mistral client
mistral_client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))

# DEFINE methods -----------------------------------------------------------

# Split text file into chunks
def get_chunks_from_text( text ):
    chunk_size = 1024
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Use Mistral embedded model to embed inputs
def get_text_embedding( inputs ):
    embeddings_batch_response = mistral_client.embeddings.create(
          model="mistral-embed",
          inputs=[inputs]
      )
    return embeddings_batch_response.data[0].embedding

# Use Mistral embedded model to loop through chunks and embed inputs
def get_chunks_embedding( chunks ):
    text_embeddings = []  
    for chunk in chunks:
        v = get_text_embedding(chunk)
        text_embeddings.append(v)
    return text_embeddings

# Use Mistral model to answer question provided with RAG context
def get_answer_from_llm( query, context ):
    prompt = f"""
    Context information is below.
    ---------------------
    {context}
    ---------------------
    You are a bot used to give people a short and simple version of a game board rules. Given the context information and not prior knowledge, answer the query. If the game is not available DO NOT answer about another game. Simply state it is not available and rules will need to be added to the knowledge base.
    Query: {query}
    Answer:
    """

    messages = [
        {
            "role": "user", "content": prompt
        }
    ]

    chat_response = mistral_client.chat.complete(
        model=model,
        messages=messages
    )
    return (chat_response.choices[0].message.content)