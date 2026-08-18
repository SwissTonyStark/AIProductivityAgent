---
name: menu-semanal
description: Planifica el menú de la semana y la lista de la compra. Úsala
  cuando el usuario pida menú, cenas de la semana o lista de la compra.
argument-hint: [restricciones, p. ej. "sin pescado, 30 min máx"]
---

# Menú semanal

Preferencias base (edítalas aquí para personalizar la skill):
- Cocina mediterránea, cenas de ≤30 minutos entre semana.
- Evitar repetir proteína dos días seguidos.

1. Aplica las restricciones extra de "$ARGUMENTS" si las hay.
2. Propón **7 cenas** (lunes–domingo) con nombre de plato y tiempo estimado;
   el fin de semana admite recetas más largas.
3. Genera la **lista de la compra** consolidada (cantidades sumadas),
   agrupada por secciones del supermercado, en formato checkbox markdown
   para poder marcarla desde el móvil.
4. Señala qué ingredientes suelen tenerse en despensa para que el usuario
   los desmarque si ya los tiene.
