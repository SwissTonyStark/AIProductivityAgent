---
name: triaje-email
description: Triaje del inbox de Gmail. Úsala cuando el usuario pida revisar,
  ordenar o ponerse al día con el correo.
argument-hint: [periodo, p. ej. "hoy" o "últimos 3 días"]
---

# Triaje de email

1. Lee los emails no leídos del periodo indicado ("$ARGUMENTS"; por defecto,
   desde ayer). Ignora promociones y notificaciones automáticas salvo que
   contengan cargos, plazos o citas.
2. Clasifica en tres pilas:
   - **Responder hoy** — requiere acción o respuesta del usuario.
   - **Puede esperar** — informativo o sin plazo inmediato.
   - **Archivar** — ruido.
3. Para cada email de "Responder hoy": redacta un **borrador** breve en el
   tono habitual del usuario (directo, cordial, en el idioma del email
   original) y déjalo como borrador en Gmail. NUNCA envíes nada.
4. Extrae **tareas implícitas** (compromisos, plazos, citas) y lístalas al
   final con fecha límite.
5. Entrega el resumen como tabla: remitente · asunto · pila · acción.
