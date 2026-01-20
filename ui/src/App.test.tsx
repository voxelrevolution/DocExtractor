import { act } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

describe("App shell", () => {
  it("renders primary navigation", () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "Documents" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Review" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Chat" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Export" })).toBeInTheDocument();
  });

  it("preserves selected document across navigation", async () => {
    const user = userEvent.setup();
    render(<App />);

    await act(async () => {
      await user.click(screen.getByRole("button", { name: /Invoice-1002/i }));
      await user.click(screen.getByRole("button", { name: "Chat" }));
      await user.click(screen.getByRole("button", { name: "Review" }));
    });

    expect(screen.getByTestId("selected-document")).toHaveTextContent("Invoice-1002");
  });

  it("shows empty state when toggled", async () => {
    const user = userEvent.setup();
    render(<App />);

    await act(async () => {
      await user.click(screen.getByRole("button", { name: "empty" }));
    });
    expect(screen.getByText("No documents yet")).toBeInTheDocument();
  });

  it("shows unsupported file error in document viewer", async () => {
    const user = userEvent.setup();
    render(<App />);

    await act(async () => {
      await user.click(screen.getByRole("button", { name: /Contract-1004/i }));
      await user.click(screen.getByRole("button", { name: "Review" }));
    });

    expect(
      screen.getByText("Unsupported file type. Please upload a PDF to view pages.")
    ).toBeInTheDocument();
  });

  it("shows empty results guidance when filters exclude all documents", async () => {
    const user = userEvent.setup();
    render(<App />);

    await act(async () => {
      await user.type(screen.getByLabelText("Search"), "NoMatchVendor");
    });

    expect(screen.getByText("No results")).toBeInTheDocument();
    expect(
      screen.getByText("Try adjusting your search or filters to find matching documents.")
    ).toBeInTheDocument();
  });
});
