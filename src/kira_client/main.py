import os

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI

from src.kira_client.genius_chain import GeniusChain

DefaultModel = "gpt-3.5-turbo-0613"


def main():
    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY is not set")

    model = os.getenv("OPENAI_MODEL") or DefaultModel

    llm = ChatOpenAI(temperature=0, model=model)

    text = "Они видят мою боль, но боятся подойти, а мне хочется всего лишь оказаться среди них"

    genius_chain = GeniusChain(llm)
    resp = genius_chain.run(text)
    print(resp)


if __name__ == "__main__":
    load_dotenv()

    main()
