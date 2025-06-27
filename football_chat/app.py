from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

API_KEY = ""  # 본인의 OpenRouter API Key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return {"response": "⚠️ 입력이 비어 있어요. 질문을 입력해주세요."}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "OpenRouter-Referer": "http://localhost",  # ✅ 정확한 Referer 헤더명
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ 현재 사용 가능한 무료 모델
        "messages": [
            {"role": "system", "content": "너는 축구 전문 AI야. 축구 관련 지식을 물으면 모두 다 알 수 있어야해."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 400,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0, read=15.0)) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            result = response.json()
            return {"response": result["choices"][0]["message"]["content"]}
    except httpx.HTTPStatusError as http_err:
        return {"response": f"❌ HTTP 오류: {http_err.response.status_code} - {http_err.response.text}"}
    except Exception as e:
        return {"response": f"❌ 에러 발생: {str(e)}"}
