type EmptyStateProps = {
  title?: string;
  description?: string;
};

export function EmptyState({ title = "No documents yet", description = "Upload documents to begin extraction." }: EmptyStateProps) {
  return (
    <div className="state-card" role="status">
      <div className="state-title">{title}</div>
      <div className="state-description">{description}</div>
    </div>
  );
}
