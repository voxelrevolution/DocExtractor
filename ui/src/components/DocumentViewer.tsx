type DocumentViewerProps = {
  filename: string;
  documentId: string | null;
  apiBaseUrl: string;
  clientId?: string;
  currentPage: number;
  totalPages: number;
  onPrev: () => void;
  onNext: () => void;
  hasError: boolean;
};

function isLocalApiBase(urlString: string): boolean {
  try {
    const parsed = new URL(urlString);
    return parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1" || parsed.hostname === "::1";
  } catch {
    return false;
  }
}

export function DocumentViewer({
  filename,
  documentId,
  apiBaseUrl,
  clientId,
  currentPage,
  totalPages,
  onPrev,
  onNext,
  hasError
}: DocumentViewerProps) {
  const localOnly = isLocalApiBase(apiBaseUrl);
  const fileUrl = documentId
    ? (() => {
        const url = new URL(`${apiBaseUrl}/api/documents/${documentId}/file`);
        if (clientId) {
          url.searchParams.set("client_id", clientId);
        }
        return url.toString();
      })()
    : null;

  return (
    <div className="viewer" aria-label="Document viewer">
      <div className="viewer-header">
        <div>
          <div className="viewer-title">Document preview</div>
          <div className="viewer-subtitle">{filename}</div>
        </div>
        <div className="viewer-controls">
          <button type="button" className="ghost-button" onClick={onPrev} disabled={currentPage <= 1}>
            Prev
          </button>
          <span className="viewer-page">Page {currentPage} of {totalPages}</span>
          <button
            type="button"
            className="ghost-button"
            onClick={onNext}
            disabled={currentPage >= totalPages}
          >
            Next
          </button>
        </div>
      </div>
      {hasError ? (
        <div className="viewer-error" role="alert">
          Unsupported file type. Please upload a PDF to view pages.
        </div>
      ) : !localOnly ? (
        <div className="viewer-error" role="alert">
          Document preview requires local API access. Set VITE_API_BASE_URL to http://localhost:8000.
        </div>
      ) : !fileUrl ? (
        <div className="viewer-canvas" role="status">
          Select a document to preview pages.
        </div>
      ) : (
        <div className="viewer-canvas" aria-label="PDF page preview">
          <iframe className="viewer-frame" title="PDF preview" src={fileUrl} />
        </div>
      )}
    </div>
  );
}
