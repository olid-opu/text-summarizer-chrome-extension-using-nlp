interface Props {
  loading: boolean;
  loadingAction: "page" | "selection" | null;
  onSummarizePage: () => void;
  onSummarizeSelection: () => void;
}

export default function ActionButtons({
  loading,
  loadingAction,
  onSummarizePage,
  onSummarizeSelection,
}: Props) {
  return (
    <div className="actions">
      <button
        type="button"
        className="btn btn-primary"
        onClick={onSummarizePage}
        disabled={loading}
      >
        {loadingAction === "page" ? (
          <>
            <span className="spinner" /> Summarizing…
          </>
        ) : (
          "Summarize Whole Page"
        )}
      </button>
      <button
        type="button"
        className="btn btn-secondary"
        onClick={onSummarizeSelection}
        disabled={loading}
      >
        {loadingAction === "selection" ? (
          <>
            <span className="spinner" /> Summarizing…
          </>
        ) : (
          "Summarize Selected Text"
        )}
      </button>
    </div>
  );
}