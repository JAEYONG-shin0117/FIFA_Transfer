from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정 (HTML 프론트엔드와 연동 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 origin 제한 권장
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 OpenRouter API Key 설정
API_KEY = "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"  # 여기에 OpenRouter에서 받은 API Key 입력

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost",  # 웹 호스팅 시 본인의 도메인으로 변경
    "Content-Type": "application/json"
}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    # OpenRouter에 사용할 메시지 구성
    body = {
        "model": "mistralai/mistral-7b-instruct",  # 다른 모델로도 교체 가능
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("https://openrouter.ai/api/v1/chat/completions",
                                    headers=HEADERS, json=body)
            res.raise_for_status()
            response = res.json()
            return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"response": f"에러 발생: {str(e)}"}
