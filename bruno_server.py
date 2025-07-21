from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for frontend → backend

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

openai.api_key = api_key

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    print(f"User said: {user_input}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Bruno, a warm, friendly assistant for TEG CIC 🌱 Your tone is down-to-earth, empowering, and emoji-rich. "
                        "You listen deeply, celebrate small wins, and help users feel supported and seen. Suggest Move, Connect, or Escape activities, "
                        "and signpost users in distress to https://tegcic.org.uk/get-help 💬💛"
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        print(f"Bruno replied: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Bruno encountered an issue: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Bruno is operational"}), 200

@app.route("/bruno_chat.html", methods=["GET"])
def serve_bruno_chat():
    return send_from_directory('.', 'bruno_chat.html')

@app.route("/", methods=["GET"])
def home():
    return redirect("/bruno_chat.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"Bruno is live at http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
