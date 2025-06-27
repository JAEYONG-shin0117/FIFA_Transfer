from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai

openai.api_key = "여기에_당신의_API_KEY"

app = FastAPI()

# CORS 설정 (로컬 테스트용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        return {"response": f"에러 발생: {str(e)}"}
