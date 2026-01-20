import type { UIState, ViewId } from "../types";

type TopBarProps = {
  viewId: ViewId;
  selectedDocumentName: string | null;
  uiState: UIState;
  onStateChange?: (state: UIState) => void;
};

const viewLabels: Record<ViewId, string> = {
  documents: "Documents",
  review: "Review",
  chat: "Chat",
  export: "Export"
};

export function TopBar({ viewId, selectedDocumentName, uiState, onStateChange }: TopBarProps) {
  const showStateToggle = import.meta.env.DEV && onStateChange;

  return (
    <header className="topbar">
      <div className="topbar-title">
        <div className="title">{viewLabels[viewId]}</div>
        <div className="subtitle" data-testid="selected-document">
          {selectedDocumentName ? `Selected: ${selectedDocumentName}` : "No document selected"}
        </div>
      </div>
      <div className="topbar-actions">
        {showStateToggle ? (
          <div className="state-toggle" aria-label="UI state toggle">
            {(["normal", "empty", "error", "loading"] as UIState[]).map((state) => (
              <button
                key={state}
                type="button"
                className={state === uiState ? "state-button active" : "state-button"}
                onClick={() => onStateChange?.(state)}
              >
                {state}
              </button>
            ))}
          </div>
        ) : null}
      </div>
    </header>
  );
}
