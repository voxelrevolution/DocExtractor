import { useMemo, useState } from "react";

type ReviewField = {
  id: string;
  label: string;
  value: string;
  warning?: string;
};

type LineItem = {
  id: string;
  description: string;
  quantity: string;
  unitPrice: string;
  amount: string;
  warning?: string;
};

type FieldReviewFormProps = {
  extractionId: string | null;
};

type SubmissionState = "idle" | "submitting" | "success" | "error" | "no-changes";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function isLocalApiBase(urlString: string): boolean {
  try {
    const parsed = new URL(urlString);
    return parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1" || parsed.hostname === "::1";
  } catch {
    return false;
  }
}

const initialHeaderFields: ReviewField[] = [
  {
    id: "vendor",
    label: "Vendor",
    value: "Northwind Supplies",
    warning: "Review required"
  },
  {
    id: "invoice_number",
    label: "Invoice #",
    value: "INV-1001"
  },
  {
    id: "invoice_date",
    label: "Invoice date",
    value: "Jan 16, 2026"
  },
  {
    id: "total",
    label: "Total",
    value: "$1,240.00",
    warning: "Check currency"
  }
];

const initialLineItems: LineItem[] = [
  {
    id: "line-1",
    description: "Consulting services",
    quantity: "2",
    unitPrice: "$300.00",
    amount: "$600.00"
  },
  {
    id: "line-2",
    description: "Hosting",
    quantity: "4",
    unitPrice: "$160.00",
    amount: "$640.00",
    warning: "Review quantity"
  }
];

export function FieldReviewForm({ extractionId }: FieldReviewFormProps) {
  const [headerFields, setHeaderFields] = useState(initialHeaderFields);
  const [lineItems, setLineItems] = useState(initialLineItems);
  const [status, setStatus] = useState<SubmissionState>("idle");
  const [message, setMessage] = useState<string | null>(null);
  const localOnly = useMemo(() => isLocalApiBase(apiBaseUrl), []);

  const changedFields = useMemo(() => {
    const headerChanges = headerFields.filter(
      (field, index) => field.value !== initialHeaderFields[index]?.value
    );
    const lineChanges = lineItems.flatMap((item, index) => {
      const original = initialLineItems[index];
      if (!original) return [];
      const changes: ReviewField[] = [];
      if (item.description !== original.description) {
        changes.push({
          id: `line_items.${index}.description`,
          label: "Line description",
          value: item.description
        });
      }
      if (item.quantity !== original.quantity) {
        changes.push({ id: `line_items.${index}.quantity`, label: "Quantity", value: item.quantity });
      }
      if (item.unitPrice !== original.unitPrice) {
        changes.push({
          id: `line_items.${index}.unit_price`,
          label: "Unit price",
          value: item.unitPrice
        });
      }
      if (item.amount !== original.amount) {
        changes.push({ id: `line_items.${index}.amount`, label: "Amount", value: item.amount });
      }
      return changes;
    });
    return { headerChanges, lineChanges };
  }, [headerFields, lineItems]);

  const handleHeaderChange = (id: string, value: string) => {
    setHeaderFields((prev) => prev.map((field) => (field.id === id ? { ...field, value } : field)));
  };

  const handleLineChange = (id: string, key: keyof LineItem, value: string) => {
    setLineItems((prev) =>
      prev.map((item) => (item.id === id ? { ...item, [key]: value } : item))
    );
  };

  const handleSubmit = async () => {
    setMessage(null);

    if (!localOnly) {
      setStatus("error");
      setMessage("Corrections require local API access. Set VITE_API_BASE_URL to http://localhost:8000.");
      return;
    }

    if (!extractionId) {
      setStatus("error");
      setMessage("No extraction selected. Choose a document before submitting corrections.");
      return;
    }

    if (changedFields.headerChanges.length === 0 && changedFields.lineChanges.length === 0) {
      setStatus("no-changes");
      setMessage("No changes to submit.");
      return;
    }

    setStatus("submitting");

    const corrections = [
      ...changedFields.headerChanges.map((field) => ({
        extraction_id: extractionId,
        field_name: field.id,
        original_value: initialHeaderFields.find((item) => item.id === field.id)?.value ?? "",
        corrected_value: field.value,
        feedback_type: "correction",
        user_notes: null
      })),
      ...changedFields.lineChanges.map((field) => ({
        extraction_id: extractionId,
        field_name: field.id,
        original_value: "",
        corrected_value: field.value,
        feedback_type: "correction",
        user_notes: null
      }))
    ];

    try {
      const response = await fetch(`${apiBaseUrl}/api/invoices/corrections`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(corrections)
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      setStatus("success");
      setMessage("Corrections saved successfully.");
    } catch (error) {
      setStatus("error");
      setMessage("Unable to submit corrections. Please try again.");
    }
  };

  return (
    <section className="review-form" aria-label="Field review form">
      <div className="review-header">
        <div>
          <h3>Review & corrections</h3>
          <p className="panel-subtitle">Edit fields, address warnings, then submit corrections.</p>
        </div>
        <button
          type="button"
          className="primary-button"
          onClick={handleSubmit}
          disabled={status === "submitting" || !localOnly || !extractionId}
        >
          {status === "submitting" ? "Submitting..." : "Submit corrections"}
        </button>
      </div>

      {message ? (
        <div
          className={
            status === "success"
              ? "status-banner success"
              : status === "error"
                ? "status-banner error"
                : "status-banner info"
          }
          role={status === "error" ? "alert" : "status"}
        >
          {message}
        </div>
      ) : null}

      <div className="review-section">
        <h4>Header fields</h4>
        <div className="review-grid">
          {headerFields.map((field) => (
            <label key={field.id} className="review-field">
              <span className="review-label">
                {field.label}
                {field.warning ? <span className="warning-pill">{field.warning}</span> : null}
              </span>
              <input
                type="text"
                value={field.value}
                onChange={(event) => handleHeaderChange(field.id, event.target.value)}
              />
            </label>
          ))}
        </div>
      </div>

      <div className="review-section">
        <h4>Line items</h4>
        <div className="line-items">
          {lineItems.map((item) => (
            <div key={item.id} className="line-item">
              <div className="line-item-row">
                <label>
                  <span>Description</span>
                  <input
                    type="text"
                    value={item.description}
                    onChange={(event) => handleLineChange(item.id, "description", event.target.value)}
                  />
                </label>
                <label>
                  <span>Qty</span>
                  <input
                    type="text"
                    value={item.quantity}
                    onChange={(event) => handleLineChange(item.id, "quantity", event.target.value)}
                  />
                </label>
                <label>
                  <span>Unit price</span>
                  <input
                    type="text"
                    value={item.unitPrice}
                    onChange={(event) => handleLineChange(item.id, "unitPrice", event.target.value)}
                  />
                </label>
                <label>
                  <span>Amount</span>
                  <input
                    type="text"
                    value={item.amount}
                    onChange={(event) => handleLineChange(item.id, "amount", event.target.value)}
                  />
                </label>
              </div>
              {item.warning ? <div className="line-warning">{item.warning}</div> : null}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
