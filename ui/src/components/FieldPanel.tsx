import { EvidencePanel } from "./EvidencePanel";

type EvidencePointer = {
  source: string;
  page?: number;
  line?: number;
  snippet?: string;
};

type FieldItem = {
  label: string;
  value: string;
  confidence: string;
  evidence?: EvidencePointer[];
  evidenceMissing?: boolean;
};

type FieldPanelProps = {
  fields: FieldItem[];
};

export function FieldPanel({ fields }: FieldPanelProps) {
  return (
    <div className="field-panel" aria-label="Extracted fields">
      <div className="viewer-title">Extracted fields</div>
      <div className="field-list">
        {fields.map((field) => (
          <div key={field.label} className="field-row">
            <div>
              <div className="field-label">{field.label}</div>
              <div className="field-value">{field.value}</div>
              {field.evidence ? (
                <EvidencePanel title="Evidence" evidence={field.evidence} />
              ) : field.evidenceMissing ? (
                <EvidencePanel title="Evidence" evidence={[]} missing />
              ) : null}
            </div>
            <div className="field-confidence">{field.confidence} Confidence</div>
          </div>
        ))}
      </div>
    </div>
  );
}
