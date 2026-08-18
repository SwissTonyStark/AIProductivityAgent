# Claude AI Factory — Playbook definitivo (agosto 2026)

> Cómo convertir tu suscripción de Claude (sin pagar tokens de API) en un asistente agéntico total — teléfono, tablet y PCs — siguiendo los patrones que usan los expertos ("AI factories" / Agent OS / asistente 24/7).

**Autor:** Pol Fernández · **Fecha:** 2026-08-18 · **Estado del ecosistema:** verificado contra docs oficiales y changelog de Claude Code v2.1.234.

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Qué ha cambiado (feb–ago 2026)](#2-qué-ha-cambiado-feb–ago-2026)
3. [Tu punto de partida: AIProductivityAgent](#3-tu-punto-de-partida-aiproductivityagent)
4. [Mapa de superficies: dónde vive Claude](#4-mapa-de-superficies-dónde-vive-claude)
5. [La regla de oro: suscripción sí, API tokens no](#5-la-regla-de-oro-suscripción-sí-api-tokens-no)
6. [Los 6 bloques de construcción](#6-los-6-bloques-de-construcción)
7. [Catálogo exhaustivo de casos de uso cotidianos](#7-catálogo-exhaustivo-de-casos-de-uso-cotidianos)
8. [La AI Factory: el Ultimate Setup por niveles](#8-la-ai-factory-el-ultimate-setup-por-niveles)
9. [Estructura de directorios y plantillas](#9-estructura-de-directorios-y-plantillas)
10. [Seguridad: lo que no puedes ignorar](#10-seguridad-lo-que-no-puedes-ignorar)
11. [Plan de acción: 30 días](#11-plan-de-acción-30-días)
12. [Fuentes](#12-fuentes)

---

## 1. Resumen ejecutivo

**La tesis:** en 2026 ya no necesitas construir tu asistente personal a mano (LangChain + Azure OpenAI + OAuth casero, como hace este repo). Anthropic ha convertido Claude en una plataforma agéntica completa donde **todo corre contra tu suscripción**: conectores nativos de Gmail/Calendar/Drive, skills reutilizables, tareas programadas en la nube (Routines), Claude Cowork para trabajo no-código, Claude Code como motor agéntico universal, y control total desde el móvil.

**Las 7 ideas clave:**

1. **Claude Code es el asistente general, no solo de código.** El Anthropic Economic Index (marzo 2026) muestra que solo ~35% del uso de Claude es programación, y el 79% de las conversaciones de Claude Code son delegación pura ("hazlo por mí"). La comunidad lo llama "coding agents are general agents".
2. **Todo con suscripción.** Claude Code con login de claude.ai, Routines, Cowork, conectores, skills, GitHub Actions (vía `claude setup-token`)… todo descuenta de tu plan Pro/Max, no de una API key. Solo necesitas API key para `claude -p --bare` y para productos construidos con el Agent SDK.
3. **Los conectores sustituyen tu código de integración.** Gmail, Google Calendar y Drive son conectores first-party disponibles en web, desktop, móvil, voz, Claude Code y Routines. Tu `gmail_client.py` y `google_calendar_client.py` son hoy un toggle en Settings.
4. **Las skills son tu know-how empaquetado.** Una carpeta con `SKILL.md` (estándar abierto agentskills.io) funciona en claude.ai, Claude Code y API. Se cargan por demanda (~100 tokens de coste fijo por skill) y se disparan solas cuando la petición encaja.
5. **La automatización sin máquina encendida existe:** Routines (nube, mín. 1h), tareas programadas de Desktop (local, mín. 1 min), `/loop` en sesión, y Cowork con tareas server-side desde julio 2026.
6. **El móvil es mando a distancia completo:** pestaña Code en la app (sesiones cloud, Remote Control por QR, Dispatch al desktop), Cowork móvil, voz con conectores (desde julio 2026 con Opus/Sonnet), y Channels (Telegram/iMessage/Discord) para chatear con una sesión de Claude Code que corre en tu PC o servidor 24/7.
7. **"AI factory" = disciplina, no magia.** Los expertos (Boris Cherny, creador de Claude Code, gestiona decenas de sesiones paralelas) construyen sobre: CLAUDE.md compartido → skills para cada bucle repetitivo → subagentes por rol → hooks deterministas → allowlists de permisos → paralelismo con worktrees/teams/workflows → verificación siempre ("duplica o triplica la calidad").

---

## 2. Qué ha cambiado (feb–ago 2026)

Cronología de lo relevante para uso personal (fuentes en §12):

| Fecha | Novedad |
|---|---|
| 5 feb | **Opus 4.6** (contexto 1M) + agent teams en Claude Code + Claude en PowerPoint (preview); mejoras Claude en Excel (Pro+) |
| 10 feb | **Cowork en Windows** (paridad con macOS) |
| feb | **Remote Control**: manejar una sesión local de Claude Code desde el móvil |
| 24–25 feb | **Plugins en Cowork** + **tareas programadas en Cowork**; **memoria gratis para todos** (incl. memoria desde historial de chats) |
| mar | **Importar memoria** desde ChatGPT/Gemini/Grok; **Dispatch** (mandar tareas desde el móvil al desktop; Pro/Max); **Channels** en preview (Telegram/Discord/iMessage) |
| 14 abr | **Routines**: tareas programadas de Claude Code en la nube (Pro/Max/Team), con triggers de cron, API y eventos GitHub |
| 16 abr | **Opus 4.7** |
| 6 may | Conferencia **Code with Claude**: Dreaming (playbooks a partir de sesiones pasadas), Outcomes, orquestación multi-agente en beta pública, **límites de 5h duplicados en Claude Code** |
| 28 may | **Opus 4.8** |
| 9 jun | **Claude Fable 5** (clase Mythos, el modelo más capaz) |
| 30 jun | **Sonnet 5** (contexto 1M, modelo por defecto en Claude Code) |
| 7–13 jul | **Cowork en web y móvil** (beta, Max primero): sesiones remotas en servidores de Anthropic, archivos sincronizados en tu cuenta, tareas programadas server-side sin dispositivo encendido |
| 20 jul | Fable 5 incluido en Max (hasta 50% del límite semanal); Pro vía créditos |
| 21 jul | **Record a Skill**: graba tu pantalla haciendo una tarea y Claude sintetiza una skill reutilizable (Pro/Max/Team) |
| 23 jul | **Voz con Opus/Sonnet y conectores**: el modo voz puede consultar tu Gmail y Calendar en mitad de la conversación |
| 24 jul | **Opus 5** (con fast mode) |
| ago | **Cowork en la barra lateral de Chrome**; sesiones de Claude in Chrome continúan entre desktop/web/móvil; Claude Code v2.1.22x: mensajería entre tus sesiones (`SendMessage` cross-session), self-hosted runners, workflows dinámicos maduros |

**Conclusión:** el semestre feb–ago 2026 cerró el círculo: cualquier tarea puede iniciarse desde cualquier dispositivo, correr en cualquier sitio (tu PC, la nube de Anthropic, un servidor tuyo) y avisarte cuando acaba.

---

## 3. Tu punto de partida: AIProductivityAgent

Este repo (LangChain + LangSmith + Azure OpenAI + clientes OAuth de Gmail/Calendar/Outlook + Streamlit) fue la forma correcta de hacerlo en 2025. En 2026, casi todo tiene equivalente nativo **sin código y sin tokens**:

| Lo que construiste | Equivalente nativo 2026 | Ventaja |
|---|---|---|
| `gmail_client.py` (OAuth + lectura + búsqueda) | **Conector Gmail** (todos los planes, incl. móvil y voz) | Cero mantenimiento, lee/busca/borradores; el envío pide confirmación |
| `google_calendar_client.py` + `generate_google_calendar_token.py` | **Conector Google Calendar** (lectura/escritura completa: crear, mover, invitar, RSVP) | Sin gestión de tokens |
| Extracción de tareas de emails (NLP) | Pedirlo en lenguaje natural, o una **skill** `email-triage` que lo estandariza | El modelo de 2026 lo hace mejor que cualquier pipeline |
| Agenda inteligente pre-reunión | **Routine** diaria ("cada mañana a las 8, cruza mi calendar con mis emails y prepárame el día") | Corre en la nube sin tu PC |
| Análisis de sentimiento | Trivial en conversación; no necesita código | — |
| Streamlit como interfaz | La app de Claude (web/desktop/móvil/voz) + Artifacts para dashboards | Multi-dispositivo gratis |
| Memoria progresiva ("actuar como tú") | **Memoria de Claude** + Proyectos + CLAUDE.md + auto-memory de Claude Code | Persistente y editable |
| Outlook (bloqueado por IT) | Sigue siendo el hueso; opciones: conector MCP de Microsoft si tu org lo permite, o mantener tu cliente como herramienta que Claude Code ejecuta | Único sitio donde tu código aporta |

**Recomendación:** congela este repo como aprendizaje y migra el valor a: (1) conectores nativos, (2) 3–4 skills que capturen tus flujos (triaje, agenda, resumen semanal), (3) una Routine matinal. Tu código de Outlook puede sobrevivir como script que Claude Code invoca localmente.

---

## 4. Mapa de superficies: dónde vive Claude

### Las superficies

- **Claude App web (claude.ai)** — chat, Proyectos, Artifacts, Research, conectores, skills, memoria, Cowork (beta), Claude Code cloud (claude.ai/code).
- **Claude Desktop (Mac/Windows)** — todo lo anterior + MCP locales (.mcpb con instalación de un clic), computer use (Pro/Max), Cowork con carpetas locales, Dispatch, tareas programadas locales, Record a Skill, app de Claude Code con pestañas Chat/Cowork/Code.
- **Claude móvil (iOS/Android)** — chat, voz (con conectores desde jul 2026), Proyectos, Artifacts, Research, Cowork remoto, pestaña **Code** (sesiones cloud + Remote Control + Dispatch), integración con apps del sistema (Recordatorios, mensajes, alarmas en Android), notificaciones push.
- **Claude Code (CLI + Desktop + web + móvil)** — el motor agéntico: acceso total a ficheros, bash, MCP, skills, subagentes, hooks, workflows.
- **Claude in Chrome** (planes de pago) — agente en panel lateral que lee, clica y rellena formularios en tus pestañas; desde ago 2026 las sesiones continúan entre dispositivos y Cowork corre en la barra lateral.
- **Modo voz** — conversación completa; desde jul 2026 con Opus/Sonnet y capaz de usar Gmail/Calendar en mitad de la charla. 18 idiomas.

### Qué usar desde cada dispositivo

| Situación | Herramienta |
|---|---|
| Andando / conduciendo | **Voz** ("¿qué tengo mañana? mueve la reunión de las 10") |
| Móvil, tarea rápida sobre email/calendar | App móvil + conectores |
| Móvil, tarea larga (organiza, investiga, redacta) | **Cowork remoto** o sesión **cloud de Claude Code** (claude.ai/code/new) — sigue corriendo con el móvil en el bolsillo |
| Móvil, quiero tocar MI PC | **Remote Control** (QR desde una sesión local) o **Dispatch** al desktop, o un **Channel de Telegram/iMessage** hacia una sesión siempre encendida |
| Tablet | claude.ai completo (Cowork + Code cloud); ideal para revisar y aprobar |
| PC, trabajo con ficheros/documentos | **Cowork** (sin terminal) o **Claude Code** (con terminal) |
| PC, navegación web repetitiva | **Claude in Chrome** |
| Nadie conectado, tarea recurrente | **Routines** (nube) o tareas programadas de Cowork server-side |

---

## 5. La regla de oro: suscripción sí, API tokens no

### Qué descuenta de la suscripción (lo que quieres)

- Claude App completa (chat, Research, voz, conectores, skills, Proyectos, Artifacts).
- **Claude Code con login de claude.ai** — CLI, Desktop, web, móvil, incluso `claude -p` en scripts y cron **mientras no uses `--bare`**.
- **Routines** y sesiones cloud (con tope diario de ejecuciones por plan).
- **GitHub Actions**: `claude setup-token` genera un OAuth token de larga duración; guárdalo como secret `CLAUDE_CODE_OAUTH_TOKEN` en `anthropics/claude-code-action@v1` y las ejecuciones facturan contra tu plan.
- **Artifacts con IA compartidos**: el consumo lo paga la suscripción de quien lo usa, no la tuya.

### Qué exige API key (lo que evitas)

- `claude -p --bare` (modo CI sin tu config).
- Productos construidos con el **Agent SDK** para terceros.
- Tu stack antiguo (LangChain + Azure OpenAI) — razón de más para jubilarlo.

### Límites (agosto 2026)

- Estructura: ventana rodante de **5 horas** + **límite semanal** (reset cada 7 días), **pool único compartido** entre App, Cowork y Claude Code. Todo cuenta: thinking, adjuntos, conectores.
- **Pro ($20)**: ≈40–80 h Sonnet/semana (estimación histórica de Anthropic); Fable 5 solo vía créditos. **Max 5x ($100)**: ≈5× por sesión, + Opus. **Max 20x ($200)**: ≈20× por sesión + más Opus; Fable 5 hasta 50% del límite semanal en Max. En mayo 2026 Anthropic **duplicó** los límites de 5h de Claude Code.
- **Extra usage** (claude.ai/settings/usage): pago por uso al agotar el plan — útil para que una Routine no muera a mitad de mes.
- `/usage` en Claude Code muestra tu consumo; en VS Code desglosa por skill/agente/plugin.

**Tácticas de ahorro:** usa Sonnet 5 por defecto y reserva Opus/Fable para planificación y problemas duros; Haiku para subagentes de búsqueda (el agente Explore ya lo hace); skills con progressive disclosure en vez de CLAUDE.md gigantes; `/compact` y sesiones limpias; Routines con prompts precisos (cada ejecución consume).

---

## 6. Los 6 bloques de construcción

### 6.1 Conectores (MCP gestionado)

- **Directorio**: claude.ai/directory (50+ integraciones): Gmail, Google Calendar, Google Drive, Notion, Slack, GitHub, Linear, Asana, Canva, Figma, Stripe, PayPal…
- **Custom connectors**: cualquier servidor MCP remoto por HTTPS → Settings → Connectors → "Add custom connector". Disponible incluso en Free (1 conector).
- **MCP local** (solo Desktop/Claude Code): bundles **.mcpb** de un clic, o `claude_desktop_config.json`, o `claude mcp add` en Claude Code con scopes `local`/`project` (`.mcp.json`)/`user`.
- Los conectores de claude.ai **se heredan en Claude Code** (v2.1.46+) y son los que usan las **Routines** en la nube. Los MCP locales NO llegan al móvil: para eso está Remote Control/Channels.
- Google publicó en 2026 servidores MCP oficiales de Workspace (Gmail 10 tools, Calendar 9, Drive 8) — alternativa avanzada a los conectores integrados.

### 6.2 Skills

- Estándar abierto (agentskills.io): carpeta + `SKILL.md` con frontmatter YAML (`name` ≤64 chars, `description` ≤1024 — la descripción decide cuándo se dispara sola).
- **Carga en 3 niveles**: metadata siempre (~100 tokens) → instrucciones al activarse (<5k) → recursos/scripts solo si se usan. Puedes tener decenas sin ensuciar el contexto.
- **En claude.ai**: Settings → Capabilities → activa "Code execution and file creation"; luego Customize → Skills → subir ZIP. Plan Pro+.
- **En Claude Code**: `~/.claude/skills/<nombre>/SKILL.md` (personales) o `.claude/skills/` (por proyecto). Los slash commands se han fusionado con las skills: `/deploy` ≡ `.claude/skills/deploy/SKILL.md`. Extras solo-Code: `disable-model-invocation`, `context: fork`, `allowed-tools`, `model`, `effort`, inyección dinámica con `` !`comando` ``, argumentos `$ARGUMENTS`.
- **Repo oficial**: github.com/anthropics/skills (~170k ★): docx, pdf, pptx, xlsx, skill-creator, mcp-builder, canvas-design, theme-factory… Instalable como marketplace: `/plugin marketplace add anthropics/skills`.
- **Record a Skill** (jul 2026): graba tu pantalla haciendo la tarea una vez → skill.
- Ojo: las skills **no se sincronizan** entre claude.ai, Claude Code y API — sube/instala en cada superficie (o usa `CLAUDE_CODE_SYNC_SKILLS=1` para bajar las de claude.ai a `~/.claude/skills/synced/`).

### 6.3 Proyectos y memoria

- **Proyectos**: instrucciones (system prompt propio) + conocimiento (ficheros); RAG automático hasta 10× capacidad en planes de pago; memoria aislada por proyecto. Crea uno por área de vida: "Casa", "Finanzas", "Salud", "Job hunting".
- **Memoria de cuenta** (gratis desde feb 2026): perfil sintetizado de tus chats, editable en Settings → Capabilities → Memory; chats de incógnito no la tocan. Import desde ChatGPT/Gemini/Grok.
- **Claude Code**: `CLAUDE.md` jerárquico (usuario → proyecto → local; imports `@fichero`; `.claude/rules/` por tema con activación por globs) + **auto memory** (`~/.claude/projects/<proyecto>/memory/MEMORY.md`) que Claude escribe solo.

### 6.4 Automatización programada

| Mecanismo | Corre en | ¿Máquina encendida? | Intervalo mín. | Ficheros locales |
|---|---|---|---|---|
| **Routines** (`/schedule`, claude.ai/code/routines) | Nube Anthropic | No | 1 h | No (clona repos) |
| **Tareas programadas Desktop/Cowork** | Tu máquina (server-side en Cowork remoto) | Sí (no en Cowork remoto) | 1 min | Sí |
| **`/loop` + cron en sesión** | Sesión abierta | Sí | 1 min | Sí |
| **cron del SO + `claude -p`** | Tu máquina/servidor | Sí | libre | Sí |
| **GitHub Actions + setup-token** | GitHub | No | libre (cron YAML) | Repo |

Routines admite además **trigger por API** (endpoint `/fire` con bearer token por routine — puedes dispararla desde Atajos de iOS, por ejemplo) y **eventos de GitHub**. Los one-shot ("`/schedule in 2 weeks…`") no cuentan contra el tope diario.

### 6.5 Channels y control remoto

- **Channels** (research preview): Telegram, Discord, iMessage (macOS, sin bot: te escribes a ti mismo). `claude --channels plugin:telegram@claude-plugins-official` → tu sesión local recibe tus mensajes, con allowlist de remitentes y relay de permisos al móvil.
- **Remote Control**: `/remote-control` en cualquier sesión local → QR → la manejas desde el móvil/web; la ejecución sigue en tu máquina; push notifications al terminar o al necesitar decisión.
- **Dispatch**: hilo persistente en el desktop; le mandas tareas desde el móvil y él decide si abre Cowork o Code (Pro/Max).
- **Cross-session messaging** (v2.1.224+): tus sesiones se mandan mensajes entre máquinas (`SendMessage`/`ListAgents`).

### 6.6 Plugins

- Paquete distribuible: skills + agentes + hooks + MCP + workflows en un repo con `.claude-plugin/plugin.json`.
- Marketplace oficial `claude-plugins-official` (auto-añadido): LSPs, integraciones (github, linear, notion, slack, sentry…), channels, `plugin-dev`, `mcp-server-dev`. Comunidad: `anthropics/claude-plugins-community`, `wshobson/agents` (~36k★), `hesreallyhim/awesome-claude-code` (~37k★), aitmpl.com.
- `/plugin` para descubrir/instalar; scopes user/project/local.

---

## 7. Catálogo exhaustivo de casos de uso cotidianos

Para cada caso: **cómo** (superficie + bloque) y madurez (🟢 probado y documentado, 🟡 funciona con montaje, 🔴 poco documentado).

### 📧 Email y comunicación 🟢
- **Triaje diario**: conector Gmail + prompt estable ("clasifica lo no leído en: responder-hoy / esperar / archivar; borradores para los primeros"). Como **Routine matinal** o skill `email-triage`. La app deja el envío tras confirmación; el borrador lo hace sola.
- **Resumen de newsletters**: Routine semanal "busca newsletters de los últimos 7 días y hazme un briefing con lo accionable".
- **Respuestas con tu tono**: Proyecto con 10–15 emails tuyos de ejemplo como conocimiento; la memoria hace el resto con el tiempo.

### 📅 Calendario y planificación 🟢
- Conector Calendar hace lectura/escritura total: crear/mover/invitar/RSVP/Meet. Por voz desde jul 2026.
- **Agenda pre-reunión** (tu caso de uso original): Routine "1h antes de cada reunión externa, cruza asistentes con mis últimos emails y prepara contexto" — o skill `prep-meeting` que invocas al momento.
- **Planificación semanal**: domingo por la noche, Routine que cruza calendar + tareas pendientes + emails marcados y propone el plan.

### ✈️ Viajes 🟢
- Research mode + web search para itinerarios (caso oficial de Anthropic); Proyecto "Viaje X" con reservas en PDF como conocimiento; Claude in Chrome para comparar precios entre pestañas; familias documentan viajes completos planificados así.

### 🍽️ Comida y compra 🟢
- Skill `meal-plan` (preferencias, alergias, súper habitual) → menú semanal + lista de compra agrupada por secciones, formato checkbox para el móvil. Documentado con Cowork sin terminal.

### 💰 Finanzas personales 🟢
- **Nivel básico**: carpeta con extractos CSV/PDF + Cowork/Claude Code: categorización, análisis 50/30/20, gráficos como Artifact. Playbook documentado ("Personal Finance Manager").
- **Nivel avanzado**: MCP de **Plaid** (bancos), **YNAB** o **Actual Budget** para datos vivos. Comunidad, no oficial: revisa el código antes de dar credenciales.
- **Impuestos**: misma mecánica sobre carpeta de facturas/recibos: clasificar, renombrar (`Factura_2026-03_Proveedor.pdf`), extraer totales a CSV con la skill oficial `xlsx`/`pdf`. 🟡

### 🏥 Salud y deporte 🟡
- MCP de wearables: AthleteData (20+ fuentes: Garmin, WHOOP, Oura, Apple Health; de pago), HealthMCP, servidores self-hosted (Open Wearables). "¿Cómo afectó mi sueño al entrenamiento esta semana?" en Desktop.
- Export de Apple Health + Claude Code → dashboard personal (patrón "Health Coach" documentado).

### 🧠 Segunda memoria / notas (Obsidian, PARA, Zettelkasten) 🟢
- El patrón estrella de la comunidad: **vault de Obsidian = memoria del agente**. Claude Code apunta a la carpeta del vault (markdown puro, sin MCP): ingesta → enlaza → cita. Repos: `AgriciDaniel/claude-obsidian` (modos LYT/PARA/Zettelkasten), `sean-esk/second-brain-gtd`, `coleam00/second-brain-starter`.
- El vault además da **contexto compartido a todos tus agentes** (patrón "Agent OS": una carpeta `Self/` con quién eres, proyectos, preferencias, que toda skill puede leer).

### 👨‍👩‍👧 Familia y hogar 🟢
- Skill "Family Operations" (tareas, menús, logística escolar, panorama semanal); página oficial de Anthropic para padres; **Home Assistant MCP** (integración nativa de HA ≥2024.10) para controlar dispositivos y crear automatizaciones hablando.

### 🛒 Compras e investigación de producto 🟢
- Claude in Chrome: lee especificaciones de varias pestañas de producto y monta tabla comparativa (caso oficial). Research mode para comparativas profundas con citas.

### 💼 CV y búsqueda de empleo 🟢
- Skills comunitarias completas: `proficiently-claude-skills` (/job-search, /tailor-resume, /cover-letter, /apply), `claude-code-job-tailor` (experiencia en YAML una vez → PDFs adaptados en <60s con ranking de requisitos).

### 🗂️ Ficheros, fotos y documentos 🟢
- **Cowork** es la herramienta: "organiza mis Descargas" (2.200 ficheros documentados en ~3 min), fotos por temática con renombrado descriptivo y cuarentena de duplicados. Skills oficiales docx/pdf/pptx/xlsx para cualquier pipeline de documentos (rellenar formularios PDF, OCR, fusionar, plantillas Word).

### 📺 Media y noticias 🟢
- Skills: YouTube Summary (transcripción yt-dlp → resumen con timestamps), Podcast Summarizer, Daily AI Brief / Morning Briefing (RSS + web search). Como Routine diaria → briefing matinal en tu Telegram (via channel) o email.

### 🗣️ Idiomas 🟢
- **Anki MCP** (AnkiConnect): "añade una tarjeta de vocabulario japonés a mi mazo" → creada con ejemplo; genera mazos desde PDFs. Modo voz para práctica conversacional.

### ⚖️ Cartas formales / disputas 🔴
- Poco documentado como caso propio; funciona como redacción genérica + skill docx + web search de normativa. El equipo legal de Anthropic usa Claude para revisar contratos.

---

## 8. La AI Factory: el Ultimate Setup por niveles

El término de la comunidad no es "AI factory" (eso es marketing de datacenters) sino **Agent OS / personal AI operating system / asistente 24/7**. La progresión que siguen los expertos:

### Nivel 0 — La App bien configurada (30 min, hazlo hoy)
1. Activa memoria (Settings → Capabilities → Memory) y "Code execution and file creation".
2. Conecta Gmail, Calendar, Drive (+ Notion/Todoist si los usas).
3. Crea 3–4 **Proyectos**: "Casa/Familia", "Finanzas", "Trabajo", "Salud" — cada uno con instrucciones y documentos clave.
4. Sube 2–3 skills al claude.ai (empieza por las del repo oficial + una tuya con skill-creator).
5. Instala Claude Desktop y la extensión de Chrome; prueba la voz con conectores.

### Nivel 1 — Claude Code como asistente local
1. Instala Claude Code y loguéate con claude.ai (nunca API key).
2. Crea tu **workspace de vida**: un repo git privado `~/life` con carpetas (`finanzas/`, `notas/` o tu vault de Obsidian, `documentos/`, `proyectos/`).
3. `~/.claude/CLAUDE.md`: quién eres, tono, reglas ("responde en español", "nunca envíes emails sin confirmar", "los ficheros de finanzas son solo-lectura salvo que lo pida").
4. Skills personales en `~/.claude/skills/`: `triaje-email`, `prep-reunion`, `resumen-semanal`, `menu-semanal`.
5. Subagentes en `~/.claude/agents/`: un `investigador` (solo lectura, modelo haiku/sonnet), un `verificador`.
6. **Permisos con allowlist, no bypass** (`/permissions`, o la skill `/fewer-permission-prompts` que la genera desde tu historial). Sandbox activado en Linux/macOS.
7. Hooks mínimos: PostToolUse que formatee/valide, Stop que verifique tareas largas.

### Nivel 2 — Automatización (la máquina trabaja sin ti)
1. **Routine matinal** (nube, corre aunque todo esté apagado): "8:00 — cruza calendar + inbox + noticias de mis temas; briefing en un gist/issue/email".
2. **Tareas programadas de Desktop** para lo que necesita tus ficheros locales (limpieza de Descargas semanal, backup de notas, informe de gastos mensual desde tu carpeta de extractos).
3. `/loop` para vigilancia en sesión ("cada 10 min mira si llegó el email de X y avísame").
4. **GitHub Actions con `claude setup-token`** para tus repos: revisión automática de PRs, issues que se auto-implementan con `@claude`.
5. Recordatorios naturales: "`/schedule` remind me in 2 weeks to renew the DNI appointment".

### Nivel 3 — Acceso desde cualquier sitio
1. Móvil: pestaña Code → sesiones cloud para tareas largas lanzadas desde el sofá.
2. **Remote Control** cuando quieras tocar tu PC desde fuera.
3. **Channel de Telegram** (o iMessage en Mac) hacia una sesión persistente en tu PC o un mini-servidor (Raspberry Pi / VPS ~13€/mes — patrón muy documentado): tu asistente 24/7 por chat, con allowlist y relay de permisos al móvil. Es la versión "de serie" de lo que este repo intentaba construir.
4. Cowork remoto para tareas de documentos desde el móvil.

### Nivel 4 — La fábrica (paralelismo y orquestación)
Los patrones de los expertos, del más simple al más potente:

- **Boris Cherny (creador de Claude Code), sus 13 prácticas**: ~5 sesiones locales en paralelo (pestañas numeradas + notificaciones del sistema) + 5–10 en la nube con `/teleport`; plan mode primero (Shift+Tab×2) y luego auto-accept; CLAUDE.md compartido en git y actualizado varias veces por semana; una skill para cada bucle interno (`/commit-push-pr`); subagentes `code-simplifier` y `verify-app`; hook de formato en PostToolUse; allowlists en vez de bypass; MCP para Slack/BigQuery/Sentry; y la regla de oro: **dale siempre a Claude una forma de verificar su trabajo — "2–3× la calidad"**.
- **Worktrees paralelos**: `claude --worktree` o subagentes con `isolation: worktree`; 4–8 en paralelo es lo sostenible — el cuello de botella eres tú revisando.
- **Agent view** (`claude agents`): panel de todas tus sesiones (corriendo/bloqueada/lista); las sesiones en background auto-commitean y abren draft PRs.
- **Agent teams** (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`): líder + 3–5 compañeros con lista de tareas compartida y buzones; debugging adversarial ("refutad las teorías de los demás").
- **Workflows dinámicos** (palabra clave `ultracode`): Claude escribe un script de orquestación (pipeline de agentes, hasta 16 concurrentes / cientos en total) — para auditorías, migraciones, investigaciones exhaustivas. `/deep-research` es uno de serie.
- **Bucle Ralph Wiggum** (Geoffrey Huntley): `while :; do cat PROMPT.md | claude -p; done` — contexto fresco cada vuelta, el estado vive en ficheros de plan, los tests son la presión de retorno. Existe como plugin oficial de demo (`ralph-wiggum`). Alternativas oficiales más controladas: `/goal` (condición de fin) y `/loop`.
- **Colas de trabajo estilo Gastown** (Steve Yegge): issues git-backed (beads), coordinador, watchdogs, merge queue — 20–30 agentes. Solo si de verdad lo necesitas.

**La escalera completa:** contexto estable (CLAUDE.md/rules) → procedimientos (skills) → roles (subagentes) → garantías deterministas (hooks) → autonomía sin fricción (allowlists+sandbox) → paralelismo (worktrees/teams/workflows) → recurrencia (loop/Routines/Actions) → control remoto (móvil/channels). Cada peldaño multiplica el anterior.

---

## 9. Estructura de directorios y plantillas

### El esqueleto de la fábrica

```
~/.claude/
├── CLAUDE.md                 # tus reglas globales (quién eres, idioma, límites)
├── settings.json             # permisos allowlist, hooks, sandbox, env
├── rules/                    # reglas por tema (finanzas.md, escritura.md)
├── skills/<nombre>/SKILL.md  # tus procedimientos (= slash commands)
├── agents/<nombre>.md        # subagentes por rol
├── loop.md                   # prompt de mantenimiento para /loop
└── projects/<repo>/memory/   # auto-memoria que Claude escribe solo

~/life/                       # tu workspace vital (repo git privado)
├── CLAUDE.md                 # mapa del workspace
├── notas/  (o vault Obsidian)
├── finanzas/extractos/
├── documentos/
└── .claude/skills/           # skills específicas del workspace
```

### Plantilla: `~/.claude/CLAUDE.md`

```markdown
# Sobre mí
- Soy Pol. Respóndeme en español; el código y los commits, en inglés.
- Zona horaria: Europe/Madrid.

# Reglas
- Nunca envíes emails ni mensajes sin enseñarme el borrador.
- Los ficheros bajo ~/life/finanzas son de solo lectura salvo petición explícita.
- Prefiere conectores nativos a scripts propios.
- Al acabar tareas largas, verifica el resultado antes de darlo por hecho.

# Mi setup
- Vault de notas: ~/life/notas (estructura PARA).
- Gestor de tareas: [tu app].
```

### Plantilla: skill `~/.claude/skills/prep-reunion/SKILL.md`

```markdown
---
name: prep-reunion
description: Prepara el contexto de una reunión. Úsala cuando pida preparar,
  repasar o llegar informado a una reunión del calendario.
argument-hint: [nombre o hora de la reunión]
---

1. Localiza la reunión "$ARGUMENTS" en Google Calendar (hoy o mañana).
2. Para cada asistente externo, busca los últimos 3 emails cruzados en Gmail.
3. Resume: objetivo probable, temas abiertos, compromisos pendientes míos,
   preguntas que me pueden hacer.
4. Entrégalo en ≤300 palabras, con una sección "Riesgos/Conflictos" si los hay.
```

### Plantilla: subagente `~/.claude/agents/investigador.md`

```markdown
---
name: investigador
description: Investiga temas en la web y en mis notas. Úsalo proactivamente
  para cualquier búsqueda amplia antes de responder.
tools: Read, Grep, Glob, WebSearch, WebFetch
model: sonnet
---
Investigas con rigor: contrasta 3+ fuentes, cita URLs, distingue hecho de
opinión, responde con un informe breve y accionable. No editas ficheros.
```

### Plantilla: `~/.claude/settings.json` (arranque prudente)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(git status)", "Bash(git diff *)", "Bash(git log *)",
      "Read(~/life/**)", "WebSearch"
    ],
    "deny": [
      "Read(./.env)", "Read(**/credentials*.json)", "Read(**/token*)"
    ]
  },
  "sandbox": { "enabled": true }
}
```

---

## 10. Seguridad: lo que no puedes ignorar

Un asistente con acceso a tu email, banca y ficheros es un objetivo. Datos de 2026: ~5,5% de servidores MCP escaneados mostraban tool poisoning; 43% de los testados eran vulnerables a inyección de comandos; en abril 2026 se secuestraron agentes (incl. Claude Code) vía títulos de PRs maliciosos.

**Reglas prácticas:**

1. **Conectores oficiales/verificados primero.** MCP comunitario (Plaid, WhatsApp, salud): lee el código antes de darle credenciales; prefiere los que guardan datos en local (el de WhatsApp usa SQLite local).
2. **OAuth con el mínimo scope** y revisa qué conectores tiene cada **Routine**: la doc oficial avisa de que en Routines Claude puede usar *todas* las herramientas del conector, escrituras incluidas, sin preguntar → quita los conectores que esa routine no necesite.
3. **Allowlists, no `bypassPermissions`.** El modo auto (GA para Max) + `deny` explícitos para `.env`, credenciales y tokens.
4. **Sandbox activado** (`/sandbox`; en Linux `bubblewrap`+`socat`) con allowlist de dominios de red.
5. **Prompt injection es real**: todo lo que Claude lee (emails, webs, PRs, resultados de tools) puede intentar redirigirlo. Las cosas irreversibles (enviar, pagar, borrar) deben pasar siempre por tu confirmación — así viene de serie: no lo desactives.
6. **Channels**: allowlist de remitentes siempre; el relay de permisos al móvil es tu freno de mano.
7. Repos ajenos: revisa sus `.claude/` (skills con `allowed-tools` se ejecutan incluso sin trust). `--safe-mode` para arrancar sin personalizaciones.

---

## 11. Plan de acción: 30 días

**Semana 1 — App (Nivel 0).** Memoria + conectores + 4 Proyectos + 2 skills subidas + Desktop y Chrome instalados. Prueba la voz con "¿qué tengo mañana?".

**Semana 2 — Claude Code (Nivel 1).** Repo `~/life`; `~/.claude/CLAUDE.md`; 3 skills personales (prep-reunion, triaje-email, resumen-semanal); subagente investigador; allowlist con `/fewer-permission-prompts`.

**Semana 3 — Automatización (Nivel 2).** Routine matinal en la nube; tarea programada local de limpieza semanal; un recordatorio one-shot; si tienes repos: claude-code-action con setup-token.

**Semana 4 — Remoto (Nivel 3).** Prueba Remote Control y una sesión cloud desde el móvil; monta el channel de Telegram hacia tu PC (o valora un Pi/VPS si quieres 24/7). Retira AIProductivityAgent: documenta en su README que sus casos de uso viven ahora en tu setup de Claude.

**Después (Nivel 4, bajo demanda).** Worktrees cuando tengas 2+ tareas paralelas reales; `ultracode`/workflows para auditorías grandes; teams solo con necesidad demostrada. Revisa `/usage` semanalmente y ajusta modelo por defecto según consumo.

---

## 12. Fuentes

**Oficiales (docs):** code.claude.com/docs (memory, settings, skills, sub-agents, hooks, mcp, plugins, routines, scheduled-tasks, desktop-scheduled-tasks, channels, remote-control, mobile, claude-code-on-the-web, agent-teams, workflows, sandboxing, github-actions, headless, feature-availability) · platform.claude.com/docs (agent-skills) · github.com/anthropics/skills · github.com/anthropics/claude-plugins-official · github.com/anthropics/claude-code (CHANGELOG) · agentskills.io · claude.ai/directory · registry.modelcontextprotocol.io

**Anuncios:** claude.com/blog (cowork-web-mobile, connectors-directory, build-artifacts, dynamic workflows) · anthropic.com/news (opus-4-6, claude-code-plugins) · anthropic.com/engineering (desktop-extensions, claude-code-best-practices, agent-skills) · Code with Claude 2026 (InfoQ)

**Expertos y comunidad:** Boris Cherny 13 tips (threads.com/@boris_cherny; digest en shanraisshan/claude-code-best-practice) · ghuntley.com/loop (Ralph Wiggum) · github.com/gastownhall/gastown · hesreallyhim/awesome-claude-code · wshobson/agents · punkpeye/awesome-mcp-servers (92k★) · zarazhang.substack.com ("coding agents are general agents") · gist de Liam Darmody (agente 24/7 en VPS) · AgriciDaniel/claude-obsidian · guías Raspberry Pi + Telegram (Medium/data-science-collective)

**Casos de uso:** claude.com/resources/use-cases (categoría Personal) · anthropic.com/for/parents · claudecodehq.com/playbooks · every.to ("Claude Code for Everyday Tasks") · theneuron.ai · Anthropic Academy (anthropic.skilljar.com — cursos gratis con certificado)

---

*Documento generado como análisis de investigación; verifica límites y disponibilidad de features en tu plan antes de depender de ellos — el ecosistema cambia cada mes.*
