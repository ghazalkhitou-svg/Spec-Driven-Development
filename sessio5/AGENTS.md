# AGENTS.md — Directives per a OpenCode

## Entorn i Stack Tècnic
- Llenguatge: Python 3.11+
- Interfície: Línia de comandes (CLI) amb mòdul `argparse` o `cmd`
- Manteniment de Dades: Fitxer JSON local (`data/tasks.json`)

## Comandes de Desenvolupament
- Executar aplicació: `python3 src/tasks_app.py`
- Executar tots els tests: `python3 -m pytest test`
- Executar test únic: `python3 -m pytest test/test_tasks_app.py`

## Convencions de Codi
- Estil: PEP8.
- Idioma del codi i comentaris: Català (mantenir consistència en noms de variables).

## Regles de Gestió de Tasques (`TASKS.md`)
1. Llegeix `TASKS.md` i identifica la següent tasca amb estat `[ ]`.
2. Canvia l'estat de la tasca actual a `[/]` abans d'iniciar la codificació.
3. Executa ÚNICAMENT una sola tasca per torn.
4. Verifica que el codi compleixi els requisits i escenaris Gherkin de `SPECIFICATIONS.md`.
5. Quan estigui completada i verificada, canvia l'estat a `[x]`.
6. Atura't i demana confirmació a l'usuari abans de passar a la següent tasca.

## Restriccions de Desenvolupament
- No instal·lis llibreries externes no autoritzades.
- No modifiquis fitxers de configuració fora de `src/` i `test/`

## Directives de l'Increment 2
- Mantén la compatibilitat amb els requisits i escenaris de l'Increment 1; no eliminis proves de regressió.
- Utilitza la biblioteca estàndard (`datetime.date`, `json`, `argparse`) i valida el format exacte i la validesa de les dates segons SPECIFICATIONS.md.
- No desis les etiquetes temporals al JSON; calcula-les amb la data local actual.
- Valida totes les dades abans de modificar el registre. No canviïs l'ID d'una tasca.
- Executa els tests amb registres temporals independents (`tmp_path`) i dates controlades o relatives. No modifiquis les dades reals del projecte durant els tests.
- Excepció a la restricció de fitxers: pots actualitzar l'estat de la tasca a TASKS.md i el JSON quan sigui imprescindible per a la tasca autoritzada. No modifiquis SPECIFICATIONS.md, AGENTS.md ni la configuració sense autorització explícita de l'usuari.
- En acabar cada tasca, mostra els fitxers modificats, les comprovacions i el resultat dels tests. Atura't perquè l'usuari revisi els canvis i faci el commit. No facis commits ni push automàticament.