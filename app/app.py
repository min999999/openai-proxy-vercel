import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ OpenAI API 키 환경변수에서 가져와 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    try:
        data = request.get_json()
        response = openai.ChatCompletion.create(**data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ OpenAI Proxy is Running"

if __name__ == "__main__":
    app.run()
