import { useState } from "react";

interface Props {
  summary: string | null;
}

export default function SummaryBox({ summary }: Props) {
  const [copied, setCopied] = useState(false);

  if (!summary) {
    return (
      <div className="card">
        <p className="empty">Your summary will appear here.</p>
      </div>
    );
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // ignore
    }
  };

  return (
    <div className="card">
      <div className="summary-head">
        <span className="summary-title">Summary</span>
        <button type="button" className="btn btn-ghost" onClick={handleCopy}>
          {copied ? "Copied!" : "Copy Summary"}
        </button>
      </div>
      <div className="summary-text">{summary}</div>
    </div>
  );
}