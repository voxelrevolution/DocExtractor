import { act } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { CopilotChat } from "./CopilotChat";

describe("CopilotChat", () => {
  it("toggles scope", async () => {
    const user = userEvent.setup();
    render(<CopilotChat />);

    expect(screen.getByRole("button", { name: "Document" })).toHaveClass("active");

    await act(async () => {
      await user.click(screen.getByRole("button", { name: "Corpus" }));
    });

    expect(screen.getByRole("button", { name: "Corpus" })).toHaveClass("active");
  });

  it("adds a response with citations", async () => {
    const user = userEvent.setup();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        reply: "The invoice total is $1,240.00. The vendor listed is Northwind Supplies.",
        citations: [
          { source: "Invoice-1001.pdf", page: 2, line: 18, snippet: "Total due: $1,240.00" }
        ]
      })
    }));
    render(<CopilotChat />);

    await act(async () => {
      await user.type(screen.getByRole("textbox"), "What is the total?");
      await user.click(screen.getByRole("button", { name: "Send" }));
    });

    expect(screen.getByText("Evidence")).toBeInTheDocument();
    expect(screen.getAllByText(/Invoice-1001.pdf/).length).toBeGreaterThan(0);
  });

  it("sends on Enter key", async () => {
    const user = userEvent.setup();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        reply: "Across the corpus, Northwind Supplies appears in 3 documents.",
        citations: [{ source: "Invoice-1001.pdf" }]
      })
    }));
    render(<CopilotChat />);

    await act(async () => {
      await user.type(screen.getByRole("textbox"), "Show totals{enter}");
    });

    expect(screen.getByText("Evidence")).toBeInTheDocument();
  });

  it("shows error banner on inference failure", async () => {
    const user = userEvent.setup();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500 }));
    render(<CopilotChat />);

    await act(async () => {
      await user.type(screen.getByRole("textbox"), "What is the total?");
      await user.click(screen.getByRole("button", { name: "Send" }));
    });

    expect(screen.getByText("Unable to run inference. Please retry in a moment.")).toBeInTheDocument();
  });
});
