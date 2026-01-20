type ErrorStateProps = {
  title?: string;
  description?: string;
  actionLabel?: string;
};

export function ErrorState({
  title = "We hit a problem",
  description = "Please retry or contact support if the issue persists.",
  actionLabel = "Retry"
}: ErrorStateProps) {
  return (
    <div className="state-card error" role="alert">
      <div className="state-title">{title}</div>
      <div className="state-description">{description}</div>
      <button className="primary-button" type="button">
        {actionLabel}
      </button>
    </div>
  );
}
