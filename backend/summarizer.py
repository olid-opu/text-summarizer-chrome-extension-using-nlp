from typing import Literal

from transformers import pipeline


SummaryType = Literal["short", "medium", "detailed"]

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
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
        self._pipeline = pipeline("summarization", model=MODEL_NAME)

    def summarize(self, text: str, summary_type: SummaryType) -> str:
        clean_text = self._normalize_text(text)
        self._validate_text(clean_text)

        min_length, max_length = SUMMARY_LENGTHS[summary_type]
        truncated_text = clean_text[:MAX_INPUT_CHARACTERS]

        result = self._pipeline(
            truncated_text,
            min_length=min_length,
            max_length=max_length,
            truncation=True,
            do_sample=False,
        )

        return result[0]["summary_text"].strip()

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def _validate_text(text: str) -> None:
        if len(text.split()) < MIN_INPUT_WORDS:
            raise SummaryInputError(
                f"Text is too short to summarize. Please provide at least {MIN_INPUT_WORDS} words."
            )
