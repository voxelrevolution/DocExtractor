import { useEffect, useMemo, useState } from "react";

type ExportRow = Record<string, string>;

type ExtractionSummary = {
  extraction_id?: string;
  vendor?: { value?: string };
  invoice_number?: { value?: string };
  invoice_date?: { value?: string };
  total_amount?: { value?: string };
  currency?: { value?: string };
  _source?: { filename?: string; document_id?: string };
};

type ExportResponse = {
  rows: ExportRow[];
};

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const clientId = (import.meta.env.VITE_DOCEXTRACTOR_CLIENT_ID ?? "").trim() || undefined;

function isLocalApiBase(urlString: string): boolean {
  try {
    const url = new URL(urlString);
    return url.hostname === "localhost" || url.hostname === "127.0.0.1" || url.hostname === "::1";
  } catch {
    return false;
  }
}

function toCsv(rows: ExportRow[]): string {
  const keys = Array.from(
    rows.reduce((set, row) => {
      Object.keys(row).forEach((key) => set.add(key));
      return set;
    }, new Set<string>())
  );

  const escape = (value: string) => {
    const needsQuotes = /[\n\r,\"]/g.test(value);
    const escaped = value.replace(/\"/g, '""');
    return needsQuotes ? `"${escaped}"` : escaped;
  };

  const header = keys.map((key) => escape(key)).join(",");
  const lines = rows.map((row) => keys.map((key) => escape(row[key] ?? "")).join(","));
  return [header, ...lines].join("\n");
}

function downloadTextFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

export function ExportPanel() {
  const [extractions, setExtractions] = useState<ExtractionSummary[]>([]);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [includeLineItems, setIncludeLineItems] = useState(true);
  const [rows, setRows] = useState<ExportRow[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const localOnly = useMemo(() => isLocalApiBase(apiBaseUrl), []);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      if (!localOnly) {
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const url = new URL(`${apiBaseUrl}/api/invoices/extractions`);
        url.searchParams.set("limit", "50");
        if (clientId) {
          url.searchParams.set("client_id", clientId);
        }

        const response = await fetch(url.toString());
        if (!response.ok) {
          throw new Error(`extractions list failed: ${response.status}`);
        }

        const data = (await response.json()) as ExtractionSummary[];
        if (!cancelled) {
          setExtractions(data);
        }
      } catch {
        if (!cancelled) {
          setError("Unable to load extractions. Ensure the local API is running.");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    };

    load();

    return () => {
      cancelled = true;
    };
  }, [localOnly]);

  const items = useMemo(() => {
    return extractions
      .map((item) => {
        const extractionId = item.extraction_id ?? "";
        const vendor = item.vendor?.value ?? "";
        const invoiceNumber = item.invoice_number?.value ?? "";
        const filename = item._source?.filename ?? "";
        const total = item.total_amount?.value ?? "";
        const currency = item.currency?.value ?? "";

        return {
          extractionId,
          vendor,
          invoiceNumber,
          filename,
          total,
          currency
        };
      })
      .filter((item) => item.extractionId);
  }, [extractions]);

  const toggleSelected = (extractionId: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(extractionId)) {
        next.delete(extractionId);
      } else {
        next.add(extractionId);
      }
      return next;
    });
  };

  const handleExport = async () => {
    setError(null);
    setInfo(null);
    setRows(null);

    if (!localOnly) {
      setError("Export is restricted to a local API base URL (localhost only).");
      return;
    }

    if (selectedIds.size === 0) {
      setError("Select at least one extraction to export.");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/invoices/export`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          extraction_ids: Array.from(selectedIds),
          include_line_items: includeLineItems,
          client_id: clientId
        })
      });

      if (!response.ok) {
        throw new Error(`export failed: ${response.status}`);
      }

      const data = (await response.json()) as ExportResponse;
      setRows(data.rows ?? []);
      setInfo(`Export ready (${data.rows?.length ?? 0} rows).`);
    } catch {
      setError("Unable to export. Ensure the local API is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadCsv = () => {
    if (!rows || rows.length === 0) {
      setError("No rows to download.");
      return;
    }

    const csv = toCsv(rows);
    const filename = `docextractor-export-${new Date().toISOString().slice(0, 10)}.csv`;
    downloadTextFile(filename, csv, "text/csv;charset=utf-8");
  };

  return (
    <section aria-label="Export panel">
      {!localOnly ? (
        <div className="status-banner error" role="alert">
          Export is restricted to local-only API access. Set VITE_API_BASE_URL to http://localhost:8000.
        </div>
      ) : null}

      {error ? (
        <div className="status-banner error" role="alert">
          {error}
        </div>
      ) : null}

      {info ? (
        <div className="status-banner success" role="status">
          {info}
        </div>
      ) : null}

      <div className="placeholder" aria-label="Export options">
        <div>
          <strong>Selections</strong>
          <div className="panel-subtitle">
            Choose which extractions to export. Exports are generated by the local API.
          </div>
        </div>

        <label>
          <input
            type="checkbox"
            checked={includeLineItems}
            onChange={(event) => setIncludeLineItems(event.target.checked)}
          />{" "}
          Include line items
        </label>

        <div>
          <button
            type="button"
            className="primary-button"
            onClick={handleExport}
            disabled={isLoading || !localOnly}
          >
            {isLoading ? "Working…" : "Run export"}
          </button>{" "}
          <button
            type="button"
            className="ghost-button"
            onClick={handleDownloadCsv}
            disabled={!rows || rows.length === 0}
          >
            Download CSV
          </button>
        </div>
      </div>

      <div className="panel-subtitle" style={{ marginTop: "var(--space-3)" }}>
        Available extractions ({items.length})
      </div>

      {items.length === 0 ? (
        <div className="placeholder">No extractions found yet. Ingest an invoice to generate extractions.</div>
      ) : (
        <div className="list" aria-label="Extractions list">
          {items.map((item) => {
            const checked = selectedIds.has(item.extractionId);
            const label = item.invoiceNumber || item.filename || item.extractionId;
            const metaParts = [item.vendor, item.total ? `${item.total} ${item.currency}`.trim() : ""].filter(Boolean);

            return (
              <label key={item.extractionId} className="list-item" style={{ display: "grid", gap: 6 }}>
                <div style={{ display: "flex", gap: "var(--space-2)", alignItems: "center" }}>
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => toggleSelected(item.extractionId)}
                    aria-label={`Select ${label}`}
                  />
                  <div>
                    <div className="list-item-title">{label}</div>
                    <div className="list-item-meta">{metaParts.join(" · ")}</div>
                  </div>
                </div>
              </label>
            );
          })}
        </div>
      )}

      {rows ? (
        <div style={{ marginTop: "var(--space-4)" }}>
          <h3>Preview</h3>
          <div className="panel-subtitle">Showing up to 10 rows.</div>
          <div className="placeholder" aria-label="Export preview">
            <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>
              {JSON.stringify(rows.slice(0, 10), null, 2)}
            </pre>
          </div>
        </div>
      ) : null}
    </section>
  );
}
