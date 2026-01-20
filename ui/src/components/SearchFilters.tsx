import type { DocumentItem } from "../types";

export type SearchFiltersState = {
  query: string;
  status: "all" | DocumentItem["status"];
  docType: "all" | "pdf" | "docx" | "other";
  dateStart: string;
  dateEnd: string;
};

type SearchFiltersProps = {
  filters: SearchFiltersState;
  onChange: (next: SearchFiltersState) => void;
  totalCount: number;
  filteredCount: number;
};

export function SearchFilters({ filters, onChange, totalCount, filteredCount }: SearchFiltersProps) {
  return (
    <div className="search-panel" aria-label="Search and filters">
      <div className="search-header">
        <div>
          <h3>Search & filters</h3>
          <p className="panel-subtitle">Find documents by vendor, invoice number, or keyword.</p>
        </div>
        <div className="search-count" aria-live="polite">
          Showing {filteredCount} of {totalCount}
        </div>
      </div>
      <div className="search-grid">
        <label className="search-field">
          <span>Search</span>
          <input
            type="text"
            value={filters.query}
            placeholder="Vendor, invoice number, keyword"
            onChange={(event) => onChange({ ...filters, query: event.target.value })}
          />
        </label>
        <label className="search-field">
          <span>Status</span>
          <select
            value={filters.status}
            onChange={(event) =>
              onChange({ ...filters, status: event.target.value as SearchFiltersState["status"] })
            }
          >
            <option value="all">All</option>
            <option value="new">New</option>
            <option value="review">Review</option>
            <option value="approved">Approved</option>
          </select>
        </label>
        <label className="search-field">
          <span>Document type</span>
          <select
            value={filters.docType}
            onChange={(event) =>
              onChange({ ...filters, docType: event.target.value as SearchFiltersState["docType"] })
            }
          >
            <option value="all">All</option>
            <option value="pdf">PDF</option>
            <option value="docx">DOCX</option>
            <option value="other">Other</option>
          </select>
        </label>
        <label className="search-field">
          <span>Start date</span>
          <input
            type="date"
            value={filters.dateStart}
            onChange={(event) => onChange({ ...filters, dateStart: event.target.value })}
          />
        </label>
        <label className="search-field">
          <span>End date</span>
          <input
            type="date"
            value={filters.dateEnd}
            onChange={(event) => onChange({ ...filters, dateEnd: event.target.value })}
          />
        </label>
      </div>
    </div>
  );
}
