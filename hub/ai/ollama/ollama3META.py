from ollama import chat
from pprint import pprint


class OllamaChat:
    def __init__(self, prompt: str) -> None:
        self.history = [{"role": "system", "content": prompt}]
        self.size = "2.0GB"

    def get(self, question: str) -> str:

        self.history.append({"role": "user", "content": question})

        response = chat(model="llama3.2", messages=self.history)

        assistant_reply = response["message"]["content"]
        self.history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def get_without_history(self, question: str) -> str:
        response = chat(
            model="llama3.2", messages=[{"role": "system", "content": question}]
        )

        return response["message"]["content"]


def main() -> None:

    ollama = OllamaChat(
        "You are a helpful assistant with knowledge about Mickey Mouse."
    )

    ollama.get_without_history("Who is Mickey Mouse?")


if __name__ == "__main__":
    main()
