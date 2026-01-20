export type ViewId = "documents" | "review" | "chat" | "export";

export type NavItem = {
  id: ViewId;
  label: string;
};

export type UIState = "normal" | "empty" | "error" | "loading";

export type DocumentItem = {
  id: string;
  name: string;
  vendor: string;
  status: "new" | "review" | "approved";
  total: string;
  updatedAt: string;
};
