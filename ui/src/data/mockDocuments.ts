import type { DocumentItem } from "../types";

export const mockDocuments: DocumentItem[] = [
  {
    id: "doc-1001",
    name: "Invoice-1001.pdf",
    vendor: "Northwind Supplies",
    status: "new",
    total: "$1,240.00",
    updatedAt: "Jan 16, 2026"
  },
  {
    id: "doc-1002",
    name: "Invoice-1002.pdf",
    vendor: "Contoso Logistics",
    status: "review",
    total: "$860.50",
    updatedAt: "Jan 16, 2026"
  },
  {
    id: "doc-1003",
    name: "Invoice-1003.pdf",
    vendor: "Fabrikam Services",
    status: "approved",
    total: "$3,410.75",
    updatedAt: "Jan 15, 2026"
  },
  {
    id: "doc-1004",
    name: "Contract-1004.docx",
    vendor: "Woodgrove Bank",
    status: "new",
    total: "$0.00",
    updatedAt: "Jan 18, 2026"
  }
];
