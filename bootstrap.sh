#!/usr/bin/env bash
# Claude AI Factory — bootstrap para macOS/Linux
# Instala las skills, el subagente y las plantillas de este repo en ~/.claude
# Idempotente: puedes ejecutarlo tras cada `git pull` para sincronizar.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "🏭 Claude AI Factory — bootstrap"
echo "   Repo:   $REPO_DIR"
echo "   Destino: $CLAUDE_DIR"

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

# Skills y agentes: se copian siempre (el repo es la fuente de verdad)
for skill in "$REPO_DIR/.claude/skills/"*/; do
  name="$(basename "$skill")"
  mkdir -p "$CLAUDE_DIR/skills/$name"
  cp -f "$skill"SKILL.md "$CLAUDE_DIR/skills/$name/SKILL.md"
  echo "   ✓ skill: /$name"
done

for agent in "$REPO_DIR/.claude/agents/"*.md; do
  cp -f "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
  echo "   ✓ agente: $(basename "$agent" .md)"
done

# Plantillas: solo si no existen (no pisamos tu configuración personal)
if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then
  cp "$REPO_DIR/setup/CLAUDE.md.plantilla" "$CLAUDE_DIR/CLAUDE.md"
  echo "   ✓ creado ~/.claude/CLAUDE.md desde plantilla — personalízalo"
else
  echo "   · ~/.claude/CLAUDE.md ya existe — no se toca"
fi

if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$REPO_DIR/setup/settings.json.plantilla" "$CLAUDE_DIR/settings.json"
  echo "   ✓ creado ~/.claude/settings.json desde plantilla"
else
  echo "   · ~/.claude/settings.json ya existe — no se toca"
fi

echo "✅ Listo. Abre 'claude' en cualquier carpeta: las skills ya están disponibles."
