import type { NavItem, ViewId } from "../types";

type NavigationProps = {
  items: NavItem[];
  activeId: ViewId;
  onChange: (viewId: ViewId) => void;
};

export function Navigation({ items, activeId, onChange }: NavigationProps) {
  return (
    <nav className="nav" aria-label="Primary">
      {items.map((item) => (
        <button
          key={item.id}
          className={item.id === activeId ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChange(item.id)}
          aria-current={item.id === activeId ? "page" : undefined}
        >
          {item.label}
        </button>
      ))}
    </nav>
  );
}
