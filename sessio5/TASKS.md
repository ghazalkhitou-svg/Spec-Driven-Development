# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (RF: RF-01, RF-02 | GS: GS-02)
- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON. (RF: RF-03, RF-04 | GS: GS-01, GS-03)
- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`). (RF: RF-01, RF-02, RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
