from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables")


client = OpenAI(api_key=api_key)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get('message')

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful female idol name pekora (เปโกะร่า). and you are very fluently and like to speak thai language , also you are very funny to talk with"},
            {"role": "user", "content": user_message}
        ]
    )

    response_message = completion.choices[0].message.content
    total_tokens = completion.usage.total_tokens
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.prompt_tokens

    cost_per_input_token = 0.0000025  # $2.50 per 1M input tokens
    cost_per_output_token = 0.00001   # $10.00 per 1M output tokens

    total_cost =( (input_tokens * cost_per_input_token) + (output_tokens * cost_per_output_token))*34

    # response_with_cost = f"{response_message} ({total_cost:.5f} บาท)"
    response_with_cost = f"{response_message} ({total_cost:.5f} )"
    return JSONResponse(content={"response": response_with_cost})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("appmain:app", host="0.0.0.0", port=8000, reload=True)