import { render, screen } from "@testing-library/react";
import { EvidencePanel } from "./EvidencePanel";

describe("EvidencePanel", () => {
  it("renders evidence pointers", () => {
    render(
      <EvidencePanel
        evidence={[{ source: "Invoice-1001.pdf", page: 2, line: 8, snippet: "Total due" }]}
      />
    );

    expect(screen.getByText(/Invoice-1001.pdf/)).toBeInTheDocument();
    expect(screen.getByText(/Page 2/)).toBeInTheDocument();
    expect(screen.getByText("Total due")).toBeInTheDocument();
  });

  it("shows missing evidence banner", () => {
    render(<EvidencePanel evidence={[]} missing />);

    expect(screen.getByText(/Evidence missing/)).toBeInTheDocument();
  });
});
