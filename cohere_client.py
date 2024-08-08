import cohere
from dotenv import load_dotenv
import os
load_dotenv()
# Initialize the Cohere client
key=os.getenv('coherence_token')
co = cohere.Client(key)

# Define a function to interact with the Cohere API
async def ask_cohere(question, prompt="你是一個回答繁體中文的全能型ai"):
    try:
        response = co.chat(
            chat_history=[
                {"role": "USER", "message": prompt}
            ],
             message=f"請用繁體中文(zh-tw)問題內容是:\n{question}",
        )
        return response.text
    except Exception as e:
        return f'An error occurred: {str(e)}'
