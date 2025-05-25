"""
test_openai.py – минимальная проверка, что ключ работает и ответы приходят.
"""

import os
import asyncio
from openai import AsyncOpenAI, OpenAI, Stream

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Не найден OPENAI_API_KEY. Экспортируй его: "
        "export OPENAI_API_KEY=sk-<your_key_here>"
    )

messages = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Привет! Скажи любую шутку про сов."},
]


def run_sync():
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    print("Ответ:", response.choices[0].message.content)


async def run_async():
    client = AsyncOpenAI(api_key=api_key)
    stream: Stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    print("Ответ (стрим): ", end="", flush=True)
    async for chunk in stream:
        delta = chunk.choices[0].delta
        print(delta.content or "", end="", flush=True)
    print()


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())