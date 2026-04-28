import { useState } from "react";
import ModeSelector from "./components/ModeSelector";
import ActionButtons from "./components/ActionButtons";
import ErrorMessage from "./components/ErrorMessage";
import SummaryBox from "./components/SummaryBox";
import { summarize, type SummaryType } from "./lib/api";
import { extractPageText } from "./lib/extractPageText";
import { extractSelectedText } from "./lib/extractSelectedText";

type ActionKind = "page" | "selection";

export default function App() {
  const [mode, setMode] = useState<SummaryType>("medium");
  const [loadingAction, setLoadingAction] = useState<ActionKind | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);

  const loading = loadingAction !== null;

  const run = async (kind: ActionKind) => {
    setError(null);
    setSummary(null);
    setLoadingAction(kind);
    try {
      const text =
        kind === "page" ? await extractPageText() : await extractSelectedText();
      const result = await summarize(text, mode, kind);
      setSummary(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <>
      <header className="header">
        <h1>AI Text Summarizer</h1>
        <p>Select text on a webpage, then click Summarize Selected Text.</p>
      </header>

      <ModeSelector value={mode} onChange={setMode} disabled={loading} />

      <ActionButtons
        loading={loading}
        loadingAction={loadingAction}
        onSummarizePage={() => run("page")}
        onSummarizeSelection={() => run("selection")}
      />

      <ErrorMessage message={error} />

      <SummaryBox summary={summary} />
    </>
  );
}