type EvidencePointer = {
  source: string;
  page?: number;
  line?: number;
  snippet?: string;
};

type EvidencePanelProps = {
  title?: string;
  evidence: EvidencePointer[];
  missing?: boolean;
  onOpenContext?: () => void;
};

export function EvidencePanel({ title = "Evidence", evidence, missing = false, onOpenContext }: EvidencePanelProps) {
  return (
    <div className={missing ? "evidence-panel missing" : "evidence-panel"}>
      <div className="evidence-header">
        <div className="evidence-title">{title}</div>
        {onOpenContext ? (
          <button type="button" className="ghost-button" onClick={onOpenContext}>
            Open context
          </button>
        ) : null}
      </div>
      {missing ? (
        <div className="evidence-missing" role="alert">
          Evidence missing. Please re-run extraction or provide a source document.
        </div>
      ) : (
        <div className="evidence-list">
          {evidence.map((item, index) => (
            <div key={`${item.source}-${index}`} className="evidence-item">
              <div className="evidence-source">
                {item.source}
                {item.page ? ` • Page ${item.page}` : ""}
                {item.line ? `, Line ${item.line}` : ""}
              </div>
              {item.snippet ? <div className="evidence-snippet">{item.snippet}</div> : null}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
