# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (RF: RF-01, RF-02 | GS: GS-02)

- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON. (RF: RF-03, RF-04 | GS: GS-01, GS-03)

- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)

- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03. (RF: RF-03, RF-04 | GS: GS-01, GS-02, GS-03)

- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`). (RF: RF-01, RF-02, RF-03, RF-04 | GS: GS-01, GS-02, GS-03)

## Increment 2: Dates límit, edició, compleció i avisos

Objectiu: Ampliar el MVP sense perdre les funcionalitats de l'Increment 1.

### Tasques d'execució (en ordre de dependències)

- [x] Tasca 2.1: Ampliar `Task` a `src/models.py` amb data límit opcional, serialització JSON i lectura de registres antics. Crear proves unitàries de serialització amb i sense data. (RF-05, RF-13; GS-04, GS-14; dependència: 1.5)

- [x] Tasca 2.2: Ampliar `add` amb `--due`, validació estricta i persistència. Afegir els tests d'alta vàlida i invàlida i compatibilitat. (RF-05, RF-06, RF-13; GS-04, GS-05, GS-14; dependència: 2.1)

- [x] Tasca 2.3: Implementar `edit --id` i l'edició parcial o múltiple dels atributs, amb validació abans de desar. Afegir tests d'edició vàlida i invàlida i d'ID inexistent per a `edit`. (RF-06, RF-07, RF-09, RF-10, RF-13; GS-06, GS-07, GS-09, GS-12, GS-13; dependència: 2.2)

- [x] Tasca 2.4: Implementar `complete --id`, incloent-hi la compleció repetida i l'error d'ID inexistent. Afegir els tests corresponents. (RF-08, RF-09, RF-13; GS-08, GS-09; dependència: 2.3)

- [x] Tasca 2.5: Ampliar `list` amb data límit i classificació temporal excloent; afegir tests de límits de dies i tasques completades o sense data. (RF-04, RF-11, RF-12, RF-13; GS-10, GS-11, GS-14, GS-15; dependència: 2.4)

- [ ] Tasca 2.6: Executar `python3 -m pytest test`, verificar tots els escenaris GS-01–GS-15, comprovar el compliment dels RF-01–RF-13 i revisar que els tests no alteren el registre real. (RF-01–RF-13; GS-01–GS-15; dependència: 2.5)

Nota: Les comprovacions que depenen d'una funcionalitat posterior es validen completament quan aquesta estigui implementada; cada tasca ha de superar les proves aplicables al seu abast.