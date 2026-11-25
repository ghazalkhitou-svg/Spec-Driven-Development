# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (RF: RF-01, RF-02 | GS: GS-02)
- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON. (RF: RF-03, RF-04 | GS: GS-01, GS-03)
- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`). (RF: RF-01, RF-02, RF-03, RF-04 | GS: GS-01, GS-02, GS-03)
- [x] Tasca 1.6: Afegir tasques a `src/tasks_app.py` amb opcions `complete` i `undo`. (RF: RF-05, RF-06 | GS: GS-04, GS-05)
- [x] Tasca 1.7: Modificar `test/test_tasks_app.py` afegint tests segons els escenaris GS-04, GS-05, GS-06, GS-07, GS-08  (RF: RF-05, RF-06 | GS: GS-04, GS-05)
- [x] Tasca 1.8: Afegir tasques a `src/tasks_app.py` amb opcions `complete` i `undo`. (RF: RF-07| GS: GS-09, GS-010)
- Tasca 1.9: Modificar `test/test_tasks_app.py` afegint tests segons els escenaris GS-09, GS-10  (RF: RF-07 | GS: GS-09, GS-10)