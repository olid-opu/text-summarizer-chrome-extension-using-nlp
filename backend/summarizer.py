import os
from typing import Literal

import openai
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
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        self.hf_token = os.environ.get("HUGGINGFACE_API_TOKEN", "").strip()

        if self.openai_api_key:
            openai.api_key = self.openai_api_key

        self.hf_headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json",
        } if self.hf_token else {"Content-Type": "application/json"}

    def summarize(self, text: str, summary_type: SummaryType) -> str:
        clean_text = self._normalize_text(text)
        self._validate_text(clean_text)

        if self.openai_api_key:
            return self._summarize_with_openai(clean_text, summary_type)

        if self.hf_token:
            return self._summarize_with_huggingface(clean_text, summary_type)

        raise SummaryInputError(
            "No inference service configured. Set OPENAI_API_KEY or HUGGINGFACE_API_TOKEN."
        )

    def _summarize_with_openai(self, text: str, summary_type: SummaryType) -> str:
        min_length, max_length = SUMMARY_LENGTHS[summary_type]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Summarize the following text in a {summary_type} style. "
                        f"Try to keep the result between {min_length} and {max_length} words.\n\n{text}"
                    ),
                },
            ],
            max_tokens=512,
            temperature=0.3,
        )

        return response.choices[0].message["content"].strip()

    def _summarize_with_huggingface(self, text: str, summary_type: SummaryType) -> str:
        min_length, max_length = SUMMARY_LENGTHS[summary_type]
        payload = {
            "inputs": text[:MAX_INPUT_CHARACTERS],
            "parameters": {
                "min_length": min_length,
                "max_length": max_length,
                "truncation": True,
            },
        }

        response = requests.post(HF_API_URL, headers=self.hf_headers, json=payload, timeout=60)
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
