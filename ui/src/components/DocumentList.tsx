import type { DocumentItem } from "../types";

type DocumentListProps = {
  documents: DocumentItem[];
  selectedId: string | null;
  onSelect: (documentId: string) => void;
};

export function DocumentList({ documents, selectedId, onSelect }: DocumentListProps) {
  return (
    <div className="list">
      {documents.map((doc) => (
        <button
          key={doc.id}
          type="button"
          className={doc.id === selectedId ? "list-item selected" : "list-item"}
          onClick={() => onSelect(doc.id)}
          aria-pressed={doc.id === selectedId}
          aria-label={`${doc.name} from ${doc.vendor}`}
        >
          <div className="list-item-title">{doc.name}</div>
          <div className="list-item-meta">
            <span>{doc.vendor}</span>
            <span className={`status status-${doc.status}`}>{doc.status}</span>
          </div>
        </button>
      ))}
    </div>
  );
}
