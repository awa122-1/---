# FJAI V1

Neuro-sama 风格 AI VTuber V1 原型。
（异想天开版）

功能：
- Web 聊天 UI
- WebSocket 实时通信
- Ollama 本地 LLM
- OpenAI-compatible LLM 接口
- SQLite 长期记忆
- 简单情绪检测
- 可选 pyttsx3 TTS
- Live2D 控制事件接口

安装：
1. Python 3.11+
2. 运行 scripts/setup.bat
3. 安装并启动 Ollama，准备一个聊天模型（默认 qwen3:4b）
4. 运行 scripts/start.bat
5. 打开 http://127.0.0.1:8765

如果使用其他 OpenAI-compatible API，修改 config/config.json。
