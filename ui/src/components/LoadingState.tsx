type LoadingStateProps = {
  title?: string;
  description?: string;
};

export function LoadingState({ title = "Loading documents", description = "Please wait while we prepare the workspace." }: LoadingStateProps) {
  return (
    <div className="state-card" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <div className="state-title">{title}</div>
      <div className="state-description">{description}</div>
    </div>
  );
}
