import logging
from flask import Flask, request, jsonify
from hub.setup.coloredprint import red, green, blue
from hub.setup.ip import get_local_ip
from hub.ai.whisper.whisperOPENAI import WhisperChat
from hub.ai.ollama.ollama3META import OllamaChat


logging.basicConfig(
    filename="log/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

api_logger = logging.getLogger("api_logger")
api_logger.setLevel(logging.DEBUG)
api_handeler = logging.FileHandler("log/api.log")
api_handeler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
api_logger.addHandler(api_handeler)


app = Flask(__name__)


@app.route("/")
def hello():
    app.logger.info("Hello route accessed")
    return "Hello World!"


@app.route("/api/text", methods=["POST"])
def api_text():
    data = request.get_json()
    try:
        prompt = data["prompt"]
        data = data["data"]
    except:
        return jsonify({"error": "No data found"})

    api_logger.info(f"Received data: {data}, prompt: {prompt}")

    # ollama = OllamaChat()

    ollama = OllamaChat(prompt=prompt)
    data = ollama.get(data)

    return jsonify(data)


@app.route("/api/audio", methods=["POST"])
def api_audio():
    if "file" in request.files:
        file = request.files["file"]
        api_logger.info(f"Received file: {file.filename}")

        extension = file.filename.split(".")[-1]
        filename = "audio." + extension

        file.save(filename)

        whisper = WhisperChat()
        response = whisper.get_response(filename)

        api_logger.info(f"Response WHISPER: {response}")

        return jsonify({"response": response})

    return jsonify({"error": request.files})


print(green(f"PORT: {get_local_ip() + ':5000'}"))


if __name__ == "__main__":
    app.logger.info(f"Starting Flask server on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
