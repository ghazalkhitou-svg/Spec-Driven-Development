import argparse
from pathlib import Path

try:
    from models import Task, tasks_from_json, tasks_to_json
except ModuleNotFoundError:
    from src.models import Task, tasks_from_json, tasks_to_json


def ruta_per_defecte() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def carregar_tasques(ruta: Path | None = None) -> list[Task]:
    fitxer = ruta if ruta is not None else ruta_per_defecte()
    if not fitxer.exists():
        fitxer.parent.mkdir(parents=True, exist_ok=True)
        fitxer.write_text("[]", encoding="utf-8")
        return []
    return tasks_from_json(fitxer.read_text(encoding="utf-8"))


def desar_tasques(tasques: list[Task], ruta: Path | None = None) -> None:
    fitxer = ruta if ruta is not None else ruta_per_defecte()
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(tasks_to_json(tasques), encoding="utf-8")


def seguent_id(tasques: list[Task]) -> int:
    return max((tasca.id for tasca in tasques), default=0) + 1


def afegir_tasca(titol: str, assignatura: str, ruta: Path | None = None) -> Task:
    tasques = carregar_tasques(ruta)
    tasca = Task(id=seguent_id(tasques), titol=titol, assignatura=assignatura)
    tasques.append(tasca)
    desar_tasques(tasques, ruta)
    return tasca


def llistar_tasques(ruta: Path | None = None) -> list[str]:
    tasques = carregar_tasques(ruta)
    if not tasques:
        return ["Registre de tasques buit."]
    return [
        f"[{tasca.id}] {tasca.titol} ({tasca.assignatura}) - estat: {tasca.estat}"
        for tasca in tasques
    ]


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasks_app",
        description="Gestiona les tasques acadèmiques.",
    )
    comandes = parser.add_subparsers(dest="comanda", required=True)

    afegir = comandes.add_parser("add", help="Afegeix una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")

    comandes.add_parser("list", help="Mostra totes les tasques")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)

    if args.comanda == "add":
        tasca = afegir_tasca(args.title, args.subject)
        print(f"Tasca [ID: {tasca.id}] creada amb èxit")
    else:
        for linia in llistar_tasques():
            print(linia)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
