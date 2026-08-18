# Claude AI Factory 🏭

Mi setup agéntico personal sobre el ecosistema Claude (suscripción, sin tokens de API): playbook, skills, subagentes y plantillas para usar Claude como asistente de verdad desde el teléfono, la tablet y **cualquier PC** — siempre el mismo setup.

> **Empieza aquí →** [`docs/CLAUDE_AI_FACTORY_PLAYBOOK.md`](docs/CLAUDE_AI_FACTORY_PLAYBOOK.md) — análisis del ecosistema (agosto 2026), catálogo completo de casos de uso y el Ultimate Setup por niveles.

## Un solo setup en todos tus PCs

La regla: **nada vive suelto en un PC**. Tres capas de sincronización:

| Capa | Qué sincroniza | Cómo |
|---|---|---|
| **Cuenta de Claude** | Memoria, Proyectos, conectores (Gmail/Calendar/Drive), skills subidas a claude.ai, Cowork remoto, sesiones cloud de Claude Code, Routines | Automático — con hacer login en cualquier dispositivo ya lo tienes |
| **Este repo (git)** | Skills de Claude Code, subagentes, plantillas de `~/.claude`, prompts de Routines | `git clone` + `./bootstrap.sh` (o `bootstrap.ps1` en Windows) en cada PC; tras un `git pull`, re-ejecuta el bootstrap |
| **Nube de ficheros** | Tu workspace vital (notas, documentos, finanzas) | Carpeta en iCloud Drive / Google Drive con el cliente de escritorio; además, el conector de Google Drive permite a Claude leerla desde cualquier superficie, móvil incluido |

Puesta en marcha en un PC nuevo (2 minutos):

```bash
git clone https://github.com/SwissTonyStark/AIProductivityAgent
cd AIProductivityAgent && ./bootstrap.sh   # Windows: .\bootstrap.ps1
claude   # login con tu cuenta de claude.ai — nunca API key
```

## Qué hay en este repo

```
├── docs/CLAUDE_AI_FACTORY_PLAYBOOK.md  # El playbook completo (léelo primero)
├── .claude/
│   ├── skills/                         # Skills (se instalan globalmente con bootstrap)
│   │   ├── prep-reunion/               #   /prep-reunion — contexto antes de una reunión
│   │   ├── triaje-email/               #   /triaje-email — clasifica el inbox y prepara borradores
│   │   ├── resumen-semanal/            #   /resumen-semanal — revisión y plan de la semana
│   │   └── menu-semanal/               #   /menu-semanal — menú + lista de la compra
│   └── agents/investigador.md          # Subagente de investigación (solo lectura)
├── setup/
│   ├── CLAUDE.md.plantilla             # → ~/.claude/CLAUDE.md (el bootstrap la copia si no existe)
│   ├── settings.json.plantilla         # → ~/.claude/settings.json (permisos prudentes + sandbox)
│   └── routines/                       # Prompts listos para claude.ai/code/routines
│       ├── briefing-matinal.md         #   laborables 07:30 — agenda + inbox + prioridades
│       └── revision-dominical.md       #   domingos 19:00 — balance + plan de semana
├── bootstrap.sh / bootstrap.ps1        # Instala todo lo anterior en ~/.claude
└── docs/
```

## La escalera (resumen del playbook)

- **Nivel 0 — App:** memoria + conectores (Gmail, Calendar, Drive) + Proyectos por área de vida + primeras skills en claude.ai.
- **Nivel 1 — Claude Code local:** este repo + bootstrap; skills y subagente disponibles en cualquier carpeta; permisos con allowlist, nunca bypass.
- **Nivel 2 — Automatización:** Routines en la nube (`setup/routines/`), tareas programadas de Desktop, `/schedule` para recordatorios.
- **Nivel 3 — Remoto:** sesiones cloud desde el móvil, Remote Control, channel de Telegram/iMessage para asistente 24/7.
- **Nivel 4 — Fábrica:** worktrees paralelos, `claude agents`, workflows `ultracode` — solo con necesidad real.

## Historia

Este repo fue **ProductivityAgent** (2025): un asistente hecho a mano con LangChain + Azure OpenAI + OAuth de Gmail/Calendar. Todo lo que hacía está hoy cubierto de forma nativa por conectores, skills y Routines de Claude — el mapa de migración está en el §3 del playbook. El código antiguo vive en el historial de git ([último commit del ProductivityAgent](../../tree/1475fd2d0367959a79a274b46816888fb24c123a)).

---

Pol Fernández · pol.fernandez.blanquez@gmail.com
