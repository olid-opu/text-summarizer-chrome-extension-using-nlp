from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from summarizer import SummaryInputError, TextSummarizer


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    summary_type: Literal["short", "medium", "detailed"]
    source_type: Literal["page", "selection"]


class SummarizeResponse(BaseModel):
    summary: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.summarizer = TextSummarizer()
    yield


app = FastAPI(title="Chrome Extension Text Summarizer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^(chrome-extension://.*|http://localhost:\d+|http://127\.0\.0\.1:\d+)$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest, request: Request) -> SummarizeResponse:
    summarizer: TextSummarizer = request.app.state.summarizer

    try:
        summary = summarizer.summarize(
            text=payload.text,
            summary_type=payload.summary_type,
        )
    except SummaryInputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SummarizeResponse(summary=summary)
