# Claude AI Factory 🏭

Mi setup agéntico personal sobre el ecosistema Claude (suscripción, sin tokens de API): playbook, skills, subagentes y plantillas de configuración para usar Claude como asistente de verdad desde el teléfono, la tablet y cualquier PC.

> **Empieza aquí →** [`docs/CLAUDE_AI_FACTORY_PLAYBOOK.md`](docs/CLAUDE_AI_FACTORY_PLAYBOOK.md) — análisis exhaustivo del ecosistema (agosto 2026), catálogo de casos de uso y el "Ultimate Setup" por niveles.

## Qué hay en este repo

```
├── docs/
│   └── CLAUDE_AI_FACTORY_PLAYBOOK.md   # El playbook completo (léelo primero)
├── .claude/
│   ├── skills/                         # Skills listas para usar en este workspace
│   │   ├── prep-reunion/               #   /prep-reunion — contexto antes de una reunión
│   │   ├── triaje-email/               #   /triaje-email — clasifica el inbox y prepara borradores
│   │   ├── resumen-semanal/            #   /resumen-semanal — revisión de la semana
│   │   └── menu-semanal/               #   /menu-semanal — menú + lista de la compra
│   └── agents/
│       └── investigador.md             # Subagente de investigación (solo lectura)
├── setup/
│   ├── CLAUDE.md.plantilla             # → copiar a ~/.claude/CLAUDE.md
│   ├── settings.json.plantilla         # → copiar a ~/.claude/settings.json
│   └── routines/                       # Prompts para crear Routines en claude.ai/code/routines
│       ├── briefing-matinal.md
│       └── revision-dominical.md
└── legacy/                             # El antiguo ProductivityAgent (LangChain, 2025) — archivado
```

## Puesta en marcha (resumen del playbook)

1. **Nivel 0 — App (30 min):** activa memoria y "Code execution and file creation"; conecta Gmail, Calendar y Drive; crea Proyectos por área de vida; sube un par de skills.
2. **Nivel 1 — Claude Code local:** login con claude.ai (nunca API key); copia las plantillas de `setup/` a `~/.claude/`; abre una sesión en este repo — las skills de `.claude/skills/` se cargan solas.
3. **Nivel 2 — Automatización:** crea las Routines de `setup/routines/` en claude.ai/code/routines; añade tareas programadas de Desktop para lo que toque ficheros locales.
4. **Nivel 3 — Remoto:** pestaña Code del móvil, Remote Control, y un channel de Telegram/iMessage si quieres asistente 24/7.
5. **Nivel 4 — Fábrica:** worktrees paralelos, `claude agents`, workflows `ultracode` — solo cuando tengas necesidad real.

Detalles, seguridad y fuentes: en el [playbook](docs/CLAUDE_AI_FACTORY_PLAYBOOK.md).

## Sobre `legacy/`

El ProductivityAgent original (LangChain + Azure OpenAI + clientes OAuth de Gmail/Calendar) queda archivado como referencia: todo lo que hacía está hoy cubierto por conectores y Routines nativos de Claude, sin código ni gestión de tokens. Ver §3 del playbook para el mapa de migración.

---

Construido por Pol Fernández (pol.fernandez.blanquez@gmail.com)
