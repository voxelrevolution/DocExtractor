#!/usr/bin/env bash
set -euo pipefail

SRC_FILES=(
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878507969.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878542778.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878580934.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878669104.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878738097.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878774234.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878831023.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878847858.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768878864986.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768879598672.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768879624156.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768879658071.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768879699110.png"
  "/home/submontain/.config/Code/User/workspaceStorage/vscode-chat-images/image-1768879726096.png"
)

DEST_BASE="/Reserved/DocExtractor/burn-pile/screenshot_inbox/2026-01-19"
mkdir -p "$DEST_BASE"

copied=0
missing=0

for src in "${SRC_FILES[@]}"; do
  if [[ -f "$src" ]]; then
    cp -n "$src" "$DEST_BASE/$(basename "$src")"
    copied=$((copied + 1))
  else
    echo "Missing: $src" >&2
    missing=$((missing + 1))
  fi
done

echo "Copied: $copied"
echo "Missing: $missing"
echo "Destination: $DEST_BASE"
