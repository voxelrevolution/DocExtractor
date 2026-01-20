import { useMemo, useState } from "react";
import type { NavItem, UIState, ViewId } from "./types";
import { mockDocuments } from "./data/mockDocuments";
import { Navigation } from "./components/Navigation";
import { DocumentList } from "./components/DocumentList";
import { DocumentViewer } from "./components/DocumentViewer";
import { FieldPanel } from "./components/FieldPanel";
import { FieldReviewForm } from "./components/FieldReviewForm";
import { CopilotChat } from "./components/CopilotChat";
import { TopBar } from "./components/TopBar";
import { EmptyState } from "./components/EmptyState";
import { ErrorState } from "./components/ErrorState";
import { LoadingState } from "./components/LoadingState";
import { ExportPanel } from "./components/ExportPanel";
import { SearchFilters, type SearchFiltersState } from "./components/SearchFilters";

const navItems: NavItem[] = [
  { id: "documents", label: "Documents" },
  { id: "review", label: "Review" },
  { id: "chat", label: "Chat" },
  { id: "export", label: "Export" }
];

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const clientId = (import.meta.env.VITE_DOCEXTRACTOR_CLIENT_ID ?? "").trim() || undefined;

const mockFields = [
  {
    label: "Vendor",
    value: "Northwind Supplies",
    confidence: "92%",
    evidence: [{ source: "Invoice-1001.pdf", page: 1, line: 6, snippet: "Vendor: Northwind Supplies" }]
  },
  {
    label: "Invoice #",
    value: "INV-1001",
    confidence: "89%",
    evidence: [{ source: "Invoice-1001.pdf", page: 1, line: 4, snippet: "Invoice # INV-1001" }]
  },
  {
    label: "Invoice date",
    value: "Jan 16, 2026",
    confidence: "94%",
    evidenceMissing: true
  },
  {
    label: "Total",
    value: "$1,240.00",
    confidence: "96%",
    evidence: [{ source: "Invoice-1001.pdf", page: 2, line: 18, snippet: "Total due: $1,240.00" }]
  }
];

export default function App() {
  const [activeView, setActiveView] = useState<ViewId>("documents");
  const [selectedId, setSelectedId] = useState<string | null>(mockDocuments[0]?.id ?? null);
  const [uiState, setUiState] = useState<UIState>("normal");
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState<SearchFiltersState>({
    query: "",
    status: "all",
    docType: "all",
    dateStart: "",
    dateEnd: ""
  });
  const totalPages = 3;

  const documents = uiState === "empty" ? [] : mockDocuments;
  const selectedDocument = useMemo(
    () => documents.find((doc) => doc.id === selectedId) ?? null,
    [documents, selectedId]
  );
  const isPdf = selectedDocument?.name.toLowerCase().endsWith(".pdf") ?? false;
  const hasViewerError = Boolean(selectedDocument && !isPdf);

  const filteredDocuments = useMemo(() => {
    const query = filters.query.trim().toLowerCase();
    return documents.filter((doc) => {
      if (filters.status !== "all" && doc.status !== filters.status) {
        return false;
      }
      if (filters.docType !== "all") {
        const ext = doc.name.split(".").pop()?.toLowerCase() ?? "";
        const docType = ext === "pdf" ? "pdf" : ext === "docx" ? "docx" : "other";
        if (docType !== filters.docType) {
          return false;
        }
      }
      if (filters.dateStart) {
        const startDate = new Date(`${filters.dateStart}T00:00:00`);
        const docDate = new Date(doc.updatedAt);
        if (!Number.isNaN(startDate.getTime()) && !Number.isNaN(docDate.getTime())) {
          if (docDate < startDate) {
            return false;
          }
        }
      }
      if (filters.dateEnd) {
        const endDate = new Date(`${filters.dateEnd}T23:59:59`);
        const docDate = new Date(doc.updatedAt);
        if (!Number.isNaN(endDate.getTime()) && !Number.isNaN(docDate.getTime())) {
          if (docDate > endDate) {
            return false;
          }
        }
      }
      if (query) {
        const haystack = `${doc.name} ${doc.vendor} ${doc.total} ${doc.status}`.toLowerCase();
        if (!haystack.includes(query)) {
          return false;
        }
      }
      return true;
    });
  }, [documents, filters]);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">DocExtractor</div>
        <Navigation items={navItems} activeId={activeView} onChange={setActiveView} />
      </aside>
      <main className="main">
        <TopBar
          viewId={activeView}
          selectedDocumentName={selectedDocument?.name ?? null}
          uiState={uiState}
          onStateChange={setUiState}
        />
        <section className="workspace">
          {uiState === "loading" ? (
            <LoadingState />
          ) : uiState === "error" ? (
            <ErrorState />
          ) : documents.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="content-grid">
              <section className="panel">
                {activeView === "documents" && (
                  <>
                    <h2>All documents</h2>
                    <p className="panel-subtitle">Select a document to view details.</p>
                    <SearchFilters
                      filters={filters}
                      onChange={setFilters}
                      totalCount={documents.length}
                      filteredCount={filteredDocuments.length}
                    />
                    {filteredDocuments.length === 0 ? (
                      <EmptyState
                        title="No results"
                        description="Try adjusting your search or filters to find matching documents."
                      />
                    ) : (
                      <DocumentList
                        documents={filteredDocuments}
                        selectedId={selectedId}
                        onSelect={setSelectedId}
                      />
                    )}
                  </>
                )}
                {activeView === "review" && (
                  <>
                    <h2>Field review</h2>
                    <p className="panel-subtitle">
                      Review extracted fields and confirm accuracy before export.
                    </p>
                    <div className="viewer-grid">
                      <DocumentViewer
                        filename={selectedDocument?.name ?? "No document selected"}
                        documentId={selectedDocument?.id ?? null}
                        apiBaseUrl={apiBaseUrl}
                        clientId={clientId}
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPrev={() => setCurrentPage((page) => Math.max(1, page - 1))}
                        onNext={() => setCurrentPage((page) => Math.min(totalPages, page + 1))}
                        hasError={hasViewerError}
                      />
                      <FieldPanel fields={mockFields} />
                    </div>
                    <FieldReviewForm extractionId={selectedDocument?.id ?? null} />
                  </>
                )}
                {activeView === "chat" && (
                  <>
                    <h2>Copilot chat</h2>
                    <p className="panel-subtitle">
                      Ask questions about the selected document or entire corpus.
                    </p>
                    <CopilotChat />
                  </>
                )}
                {activeView === "export" && (
                  <>
                    <h2>Export</h2>
                    <p className="panel-subtitle">Prepare CSV or Excel exports.</p>
                    <ExportPanel />
                  </>
                )}
              </section>
              <section className="panel secondary">
                <h2>Document context</h2>
                <p className="panel-subtitle">
                  {selectedDocument
                    ? "Evidence, metadata, and workflow status for the selected document."
                    : "Select a document to view details."}
                </p>
                {selectedDocument ? (
                  <div className="detail-grid">
                    <div>
                      <div className="detail-label">File</div>
                      <div className="detail-value">{selectedDocument.name}</div>
                    </div>
                    <div>
                      <div className="detail-label">Vendor</div>
                      <div className="detail-value">{selectedDocument.vendor}</div>
                    </div>
                    <div>
                      <div className="detail-label">Status</div>
                      <div className="detail-value">{selectedDocument.status}</div>
                    </div>
                    <div>
                      <div className="detail-label">Total</div>
                      <div className="detail-value">{selectedDocument.total}</div>
                    </div>
                    <div>
                      <div className="detail-label">Updated</div>
                      <div className="detail-value">{selectedDocument.updatedAt}</div>
                    </div>
                  </div>
                ) : null}
              </section>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
