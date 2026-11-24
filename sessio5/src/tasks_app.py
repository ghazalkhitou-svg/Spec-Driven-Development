import argparse
import sys
from pathlib import Path

try:
    from models import (
        Task,
        tasks_from_json,
        tasks_to_json,
        validar_data_limit,
        validar_estat,
    )
except ModuleNotFoundError:
    from src.models import (
        Task,
        tasks_from_json,
        tasks_to_json,
        validar_data_limit,
        validar_estat,
    )


def ruta_per_defecte() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def carregar_tasques(
    ruta: Path | None = None,
    *,
    crear_si_falta: bool = True,
) -> list[Task]:
    fitxer = ruta if ruta is not None else ruta_per_defecte()
    if not fitxer.exists():
        if not crear_si_falta:
            return []
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


def afegir_tasca(
    titol: str,
    assignatura: str,
    ruta: Path | None = None,
    data_limit: str | None = None,
) -> Task:
    validar_data_limit(data_limit)
    tasques = carregar_tasques(ruta)
    tasca = Task(
        id=seguent_id(tasques),
        titol=titol,
        assignatura=assignatura,
        data_limit=data_limit,
    )
    tasques.append(tasca)
    desar_tasques(tasques, ruta)
    return tasca


def cercar_tasca(tasques: list[Task], id_tasca: int) -> Task:
    tasca = next((item for item in tasques if item.id == id_tasca), None)
    if tasca is None:
        raise ValueError(f"No existeix la tasca amb ID {id_tasca}.")
    return tasca


def editar_tasca(
    id_tasca: int,
    titol: str | None = None,
    assignatura: str | None = None,
    data_limit: str | None = None,
    estat: str | None = None,
    ruta: Path | None = None,
) -> Task:
    validar_data_limit(data_limit)
    validar_estat(estat)
    if all(
        valor is None
        for valor in (titol, assignatura, data_limit, estat)
    ):
        raise ValueError("Cal indicar almenys un atribut per modificar.")

    tasques = carregar_tasques(ruta, crear_si_falta=False)
    tasca = cercar_tasca(tasques, id_tasca)

    if titol is not None:
        tasca.titol = titol
    if assignatura is not None:
        tasca.assignatura = assignatura
    if data_limit is not None:
        tasca.data_limit = data_limit
    if estat is not None:
        tasca.estat = estat

    desar_tasques(tasques, ruta)
    return tasca


def completar_tasca(id_tasca: int, ruta: Path | None = None) -> Task:
    tasques = carregar_tasques(ruta, crear_si_falta=False)
    tasca = cercar_tasca(tasques, id_tasca)
    tasca.estat = "completada"
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
    afegir.add_argument(
        "--due",
        default=None,
        help="Data límit opcional en format YYYY-MM-DD",
    )

    editar = comandes.add_parser("edit", help="Modifica una tasca existent")
    editar.add_argument(
        "--id",
        type=int,
        required=True,
        help="Identificador de la tasca",
    )
    editar.add_argument(
        "--title",
        default=None,
        help="Títol nou de la tasca",
    )
    editar.add_argument(
        "--subject",
        default=None,
        help="Assignatura nova de la tasca",
    )
    editar.add_argument(
        "--due",
        default=None,
        help="Data límit nova en format YYYY-MM-DD",
    )
    editar.add_argument(
        "--status",
        default=None,
        help="Estat nou de la tasca",
    )

    completar = comandes.add_parser(
        "complete",
        help="Marca una tasca com a completada",
    )
    completar.add_argument(
        "--id",
        type=int,
        required=True,
        help="Identificador de la tasca",
    )

    comandes.add_parser("list", help="Mostra totes les tasques")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)

    try:
        if args.comanda == "add":
            tasca = afegir_tasca(args.title, args.subject, data_limit=args.due)
            print(f"Tasca [ID: {tasca.id}] creada amb èxit")
        elif args.comanda == "edit":
            tasca = editar_tasca(
                args.id,
                titol=args.title,
                assignatura=args.subject,
                data_limit=args.due,
                estat=args.status,
            )
            print(f"Tasca [ID: {tasca.id}] modificada amb èxit")
        elif args.comanda == "complete":
            tasca = completar_tasca(args.id)
            print(f"Tasca [ID: {tasca.id}] completada amb èxit")
        else:
            for linia in llistar_tasques():
                print(linia)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
