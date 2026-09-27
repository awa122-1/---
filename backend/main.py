import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.ai.brain import AIBrain
from backend.emotion.detector import EmotionDetector
from backend.live2d.controller import Live2DController
from backend.server.events import event
from backend.tts.engine import TTSEngine
from backend.utils.config import load_config

ROOT = Path(__file__).resolve().parents[1]
config = load_config(ROOT / "config" / "config.json")
brain = AIBrain(ROOT, config)
emotion = EmotionDetector(ROOT / "config" / "emotions.json")
tts = TTSEngine(ROOT, config)
live2d = Live2DController()

app = FastAPI(title="FJAI V1")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")
app.mount("/audio", StaticFiles(directory=ROOT / "audio" / "output"), name="audio")

@app.get("/")
async def index():
    return FileResponse(ROOT / "frontend" / "index.html")

@app.get("/api/health")
async def health():
    return {"ok": True, "name": "FJAI", "version": "V1"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_json(event("system", {"message": "芙酱AI已连接。"}))
    try:
        while True:
            payload = json.loads(await ws.receive_text())
            if payload.get("type") != "chat":
                continue
            user_text = str(payload.get("message", "")).strip()
            if not user_text:
                continue

            await ws.send_json(event("thinking", {"value": True}))
            try:
                result = await brain.chat(user_text)
                emo = emotion.detect(user_text + " " + result["text"])
                await ws.send_json(event("emotion", live2d.expression_event(emo)))
                await ws.send_json(event("message", {
                    "role": "assistant",
                    "text": result["text"],
                    "emotion": emo,
                    "memory_saved": result["memory_saved"]
                }))
                audio = await tts.speak(result["text"])
                if audio:
                    await ws.send_json(event("audio", {"url": audio}))
            except Exception as exc:
                await ws.send_json(event("error", {"message": str(exc)}))
            finally:
                await ws.send_json(event("thinking", {"value": False}))
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host=config["server"]["host"], port=int(config["server"]["port"]))
