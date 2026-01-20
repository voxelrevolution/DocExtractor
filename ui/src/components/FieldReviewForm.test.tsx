import { act } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { FieldReviewForm } from "./FieldReviewForm";

describe("FieldReviewForm", () => {
  it("shows warnings on required fields", () => {
    render(<FieldReviewForm extractionId="doc-1001" />);

    expect(screen.getByText("Review required")).toBeInTheDocument();
    expect(screen.getByText("Check currency")).toBeInTheDocument();
  });

  it("submits corrections and shows success", async () => {
    const user = userEvent.setup();
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => []
    } as Response);

    render(<FieldReviewForm extractionId="doc-1001" />);

    const invoiceField = screen.getByLabelText("Invoice #");

    await act(async () => {
      await user.clear(invoiceField);
      await user.type(invoiceField, "INV-1001A");
      await user.click(screen.getByRole("button", { name: "Submit corrections" }));
    });

    expect(fetchSpy).toHaveBeenCalledWith(
      "http://localhost:8000/api/invoices/corrections",
      expect.objectContaining({ method: "POST" })
    );
    expect(screen.getByText("Corrections saved successfully.")).toBeInTheDocument();

    fetchSpy.mockRestore();
  });
});
