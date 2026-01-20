import { act } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { ExportPanel } from "./ExportPanel";

describe("ExportPanel", () => {
  it("loads extractions and runs an export", async () => {
    const user = userEvent.setup();

    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [
            {
              extraction_id: "ex-1",
              vendor: { value: "Northwind Supplies" },
              invoice_number: { value: "INV-1001" },
              total_amount: { value: "10.00" },
              currency: { value: "USD" },
              _source: { filename: "invoice.pdf" }
            }
          ]
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            rows: [{ extraction_id: "ex-1", vendor: "Northwind Supplies" }]
          })
        })
    );

    render(<ExportPanel />);

    expect(await screen.findByText(/Available extractions \(1\)/i)).toBeInTheDocument();

    await act(async () => {
      await user.click(screen.getByRole("checkbox", { name: /Select INV-1001/i }));
      await user.click(screen.getByRole("button", { name: /Run export/i }));
    });

    expect(screen.getByText(/Export ready/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Northwind Supplies/i).length).toBeGreaterThan(0);

    const fetchMock = (globalThis.fetch as unknown as ReturnType<typeof vi.fn>);
    expect(fetchMock).toHaveBeenCalledWith(expect.stringMatching(/\/api\/invoices\/extractions/));
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringMatching(/\/api\/invoices\/export/),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("shows a helpful error when exporting with no selection", async () => {
    const user = userEvent.setup();

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => []
      })
    );

    render(<ExportPanel />);

    expect(await screen.findByText(/Available extractions \(0\)/i)).toBeInTheDocument();

    await act(async () => {
      await user.click(screen.getByRole("button", { name: /Run export/i }));
    });

    expect(screen.getByText("Select at least one extraction to export.")).toBeInTheDocument();
  });
});
