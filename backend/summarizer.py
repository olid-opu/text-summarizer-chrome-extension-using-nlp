import os
from typing import Literal

import requests


SummaryType = Literal["short", "medium", "detailed"]

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
MIN_INPUT_WORDS = 20
MAX_INPUT_CHARACTERS = 6000

SUMMARY_LENGTHS: dict[SummaryType, tuple[int, int]] = {
    "short": (30, 70),
    "medium": (60, 130),
    "detailed": (100, 220),
}


class SummaryInputError(ValueError):
    pass


class TextSummarizer:
    def __init__(self) -> None:
        token = os.environ.get("HUGGINGFACE_API_TOKEN", "").strip()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        } if token else {"Content-Type": "application/json"}

    def summarize(self, text: str, summary_type: SummaryType) -> str:
        clean_text = self._normalize_text(text)
        self._validate_text(clean_text)

        min_length, max_length = SUMMARY_LENGTHS[summary_type]
        payload = {
            "inputs": clean_text[:MAX_INPUT_CHARACTERS],
            "parameters": {
                "min_length": min_length,
                "max_length": max_length,
                "truncation": True,
            },
        }

        response = requests.post(HF_API_URL, headers=self.headers, json=payload, timeout=60)
        if response.status_code != 200:
            raise SummaryInputError(
                f"Hugging Face inference failed ({response.status_code}): {response.text}"
            )

        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            raise SummaryInputError(f"Hugging Face inference error: {data['error']}")
        if not isinstance(data, list) or not data or "generated_text" not in data[0]:
            raise SummaryInputError("Invalid summarization response from Hugging Face.")

        return data[0]["generated_text"].strip()

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def _validate_text(text: str) -> None:
        if len(text.split()) < MIN_INPUT_WORDS:
            raise SummaryInputError(
                f"Text is too short to summarize. Please provide at least {MIN_INPUT_WORDS} words."
            )
