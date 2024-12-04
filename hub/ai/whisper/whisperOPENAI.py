import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


import whisper


class WhisperChat:
    def __init__(self):
        self.model = whisper.load_model("medium")

    def get_response(self, file: str):
        return self.model.transcribe(file)["text"]


def main() -> None:
    chat = WhisperChat()
    print(chat.get_response("audio.wav"))


if __name__ == "__main__":
    main()
