export type SummaryType = "short" | "medium" | "detailed";
export type SourceType = "page" | "selection";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const API_URL = `${API_BASE_URL.replace(/\/$/, "")}/summarize`;

export async function summarize(
  text: string,
  summary_type: SummaryType,
  source_type: SourceType,
): Promise<string> {
  let res: Response;
  try {
    res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, summary_type, source_type }),
    });
  } catch {
    throw new Error(
      `Failed to reach summarizer service at ${API_BASE_URL}.`,
    );
  }

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const data = (await res.json()) as { detail?: string; error?: string };
      message = data.detail || data.error || message;
    } catch {
      // ignore
    }
    throw new Error(message);
  }

  const data = (await res.json()) as { summary?: string };
  if (!data.summary) {
    throw new Error("Backend returned an empty summary.");
  }
  return data.summary;
}
