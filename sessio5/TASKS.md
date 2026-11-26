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

- [x] Tasca 1.9: Modificar `test/test_tasks_app.py` afegint tests segons els escenaris GS-09, GS-10  (RF: RF-07 | GS: GS-09, GS-10)

## Increment 2: Dates límit, edició, compleció i avisos

Objectiu: Ampliar el MVP sense perdre les funcionalitats de l'Increment 1.

### Tasques d'execució (en ordre de dependències)

- [x] Tasca 2.1: Ampliar `Task` a `src/models.py` amb data límit opcional, serialització JSON i lectura de registres antics. Crear proves unitàries de serialització amb i sense data. (RF-05, RF-13; GS-11, GS-21; dependència: 1.5)

- [x] Tasca 2.2: Ampliar `add` amb `--due`, validació estricta i persistència. Afegir els tests d'alta vàlida i invàlida i compatibilitat. (RF-08, RF-09, RF-16; GS-11, GS-12, GS-21; dependència: 2.1)

- [x] Tasca 2.3: Implementar `edit --id` i l'edició parcial o múltiple dels atributs, amb validació abans de desar. Afegir tests d'edició vàlida i invàlida i d'ID inexistent per a `edit`. (RF-09, RF-10, RF-12, RF-13, RF-16; GS-13, GS-14, GS-16, GS-19, GS-20; dependència: 2.2)

- [x] Tasca 2.4: Implementar `complete --id`, incloent-hi la compleció repetida i l'error d'ID inexistent. Afegir els tests corresponents. (RF-11, RF-12, RF-16; GS-15, GS-16; dependència: 2.3)

- [x] Tasca 2.5: Ampliar `list` amb data límit i classificació temporal excloent; afegir tests de límits de dies i tasques completades o sense data. (RF-04, RF-14, RF-15, RF-16; GS-17, GS-18, GS-21, GS-22; dependència: 2.4)

- [x] Tasca 2.6: Executar `python3 -m pytest test`, verificar tots els escenaris GS-01–GS-22, comprovar el compliment dels RF-01–RF-13 i revisar que els tests no alteren el registre real. (RF-01–RF-16; GS-01–GS-22; dependència: 2.5)

## Increment 3: Resum, filtratge per assignatura, filtratge per paraula clau
- Tasca 3.1: Ampliar `list` amb `--short`. (RF: RF-17 | GS: GS-23)

- Tasca 3.2: A `test/test_tasks_app.py` afegir els tests dels escenaris GS-23

- Tasca 3.3: Tasca 3.3: Ampliar `list` amb `--subject`. (RF: RF-18 | GS: GS-24, GS-25)

- Tasca 3.4: A `test/test_tasks_app.py` afegir els tests dels escenaris GS-24 i GS-25

- Tasca 3.5: Tasca 3.3: `list` amb `--find`. (RF: RF-19 | GS: GS-26, GS-27)

- Tasca 3.6: A `test/test_tasks_app.py` afegir els tests dels escenaris GS-26 i GS-27