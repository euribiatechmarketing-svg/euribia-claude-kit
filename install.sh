#!/usr/bin/env bash
# Euribia Claude kit installer (macOS).
# Copies skills, agents, contento playbooks and brand fonts into ~/.claude,
# then installs the shared plugins. Safe to re-run: anything it replaces is
# backed up to ~/.claude/backups/kit-<date>/ first.
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BACKUP="$CLAUDE_DIR/backups/kit-$(date +%Y%m%d-%H%M%S)"

say() { printf '\033[1;35m==>\033[0m %s\n' "$*"; }

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

backup_if_exists() {   # $1 = path inside CLAUDE_DIR
  local target="$CLAUDE_DIR/$1"
  if [ -e "$target" ]; then
    mkdir -p "$BACKUP/$(dirname "$1")"
    cp -R "$target" "$BACKUP/$1"
  fi
}

say "Skills"
for dir in "$KIT"/skills/*/; do
  name="$(basename "$dir")"
  backup_if_exists "skills/$name"
  rm -rf "$CLAUDE_DIR/skills/$name"
  cp -R "$dir" "$CLAUDE_DIR/skills/$name"
  echo "   $name"
done

say "Agents"
for f in "$KIT"/agents/*.md; do
  backup_if_exists "agents/$(basename "$f")"
  cp "$f" "$CLAUDE_DIR/agents/"
  echo "   $(basename "$f" .md)"
done

say "Contento playbooks and brand assets"
backup_if_exists "contento"
# Keep any local state (ledger etc.) the colleague already has.
rsync -a --exclude 'state/ledger*.json' --exclude 'state/postflow.json' "$KIT/contento/" "$CLAUDE_DIR/contento/"

say "Brand fonts (Mulish, Azeret Mono)"
mkdir -p "$HOME/Library/Fonts"
cp -n "$KIT"/fonts/*.ttf "$HOME/Library/Fonts/" 2>/dev/null || true

say "API keys file"
mkdir -p "$HOME/.config/euribia"
if [ ! -f "$HOME/.config/euribia/api-keys.env" ]; then
  cp "$KIT/.env.example" "$HOME/.config/euribia/api-keys.env"
  chmod 600 "$HOME/.config/euribia/api-keys.env"
  echo "   created ~/.config/euribia/api-keys.env (fill in the values)"
else
  echo "   ~/.config/euribia/api-keys.env already exists, left as is"
fi

say "Plugins"
if command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add anthropics/claude-plugins-official || true
  claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill || true
  claude plugin install superpowers@claude-plugins-official || true
  claude plugin install ui-ux-pro-max@ui-ux-pro-max-skill || true
else
  echo "   'claude' not found. Install Claude Code first (see README), then re-run."
fi

[ -d "$BACKUP" ] && say "Old versions backed up to $BACKUP"
say "Done. Restart Claude Code / T3 Code to load the skills."
