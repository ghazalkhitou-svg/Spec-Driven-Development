import argparse
import sys
from datetime import date
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


def missatge_no_existeix(id_tasca: int) -> str:
    return f"Tasca [ID: {id_tasca}] no existeix"


def cercar_tasca(tasques: list[Task], id_tasca: int) -> Task:
    tasca = next((item for item in tasques if item.id == id_tasca), None)
    if tasca is None:
        raise ValueError(f"No existeix la tasca amb ID {id_tasca}.")
    return tasca


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


def aplicar_estat(
    id_tasca: int, estat_objectiu: str, ruta: Path | None = None
) -> bool:
    """Canvia l'estat d'una tasca.

    Retorna True si l'estat ha canviat i False si ja era l'estat objectiu.
    Llança ValueError si la tasca no existeix.
    """
    tasques = carregar_tasques(ruta, crear_si_falta=False)
    tasca = cercar_tasca(tasques, id_tasca)
    if tasca.estat == estat_objectiu:
        return False
    tasca.estat = estat_objectiu
    desar_tasques(tasques, ruta)
    return True


def missatge_estat(id_tasca: int, estat_objectiu: str, canviat: bool) -> str:
    if not canviat:
        return f"Tasca [ID: {id_tasca}] ja està marcada com a {estat_objectiu}"
    if estat_objectiu == "completada":
        return f"Tasca [ID: {id_tasca}] completada amb èxit"
    return f"Tasca [ID: {id_tasca}] marcada com a {estat_objectiu}"


def canviar_estat(
    id_tasca: int, estat_objectiu: str, ruta: Path | None = None
) -> str:
    try:
        canviat = aplicar_estat(id_tasca, estat_objectiu, ruta)
    except ValueError:
        return missatge_no_existeix(id_tasca)
    return missatge_estat(id_tasca, estat_objectiu, canviat)


def eliminar_tasca(id_tasca: int, ruta: Path | None = None) -> str:
    tasques = carregar_tasques(ruta)
    for posicio, tasca in enumerate(tasques):
        if tasca.id == id_tasca:
            del tasques[posicio]
            desar_tasques(tasques, ruta)
            return f"Tasca [ID: {id_tasca}] eliminada amb èxit"
    return missatge_no_existeix(id_tasca)


def etiqueta_temporal(tasca: Task, avui: date) -> str | None:
    if tasca.estat != "pendent" or tasca.data_limit is None:
        return None
    data_limit = date.fromisoformat(tasca.data_limit)
    dies = (data_limit - avui).days
    if dies < 0:
        return "[CADUCADA]"
    if dies <= 6:
        return "[URGENT]"
    return None


def resum_tasques(ruta: Path | None = None, avui: date | None = None) -> list[str]:
    tasques = carregar_tasques(ruta)
    data_actual = avui if avui is not None else date.today()
    total = len(tasques)
    completades = 0
    pendents = 0
    urgents = 0
    caducades = 0
    for tasca in tasques:
        if tasca.estat == "completada":
            completades += 1
            continue
        etiqueta = etiqueta_temporal(tasca, data_actual)
        if etiqueta == "[CADUCADA]":
            caducades += 1
        elif etiqueta == "[URGENT]":
            urgents += 1
        else:
            pendents += 1
    return [
        f"Nombre total de tasques: {total}",
        f"Nombre total de tasques pendents: {pendents}",
        f"Nombre total de tasques completades: {completades}",
        f"Nombre total de tasques urgents: {urgents}",
        f"Nombre total de tasques caducades: {caducades}",
    ]


def llistar_tasques(ruta: Path | None = None, avui: date | None = None) -> list[str]:
    tasques = carregar_tasques(ruta)
    if not tasques:
        return ["Registre de tasques buit."]

    data_actual = avui if avui is not None else date.today()
    linies: list[str] = []
    for tasca in tasques:
        linia = (
            f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
            f" - estat: {tasca.estat}"
        )
        if tasca.data_limit is not None:
            linia += f" - data límit: {tasca.data_limit}"
        etiqueta = etiqueta_temporal(tasca, data_actual)
        if etiqueta is not None:
            linia += f" {etiqueta}"
        linies.append(linia)
    return linies


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
    editar.add_argument("--id", type=int, required=True, help="ID de la tasca")
    editar.add_argument("--title", default=None, help="Títol nou de la tasca")
    editar.add_argument(
        "--subject", default=None, help="Assignatura nova de la tasca"
    )
    editar.add_argument(
        "--due",
        default=None,
        help="Data límit nova en format YYYY-MM-DD",
    )
    editar.add_argument("--status", default=None, help="Estat nou de la tasca")

    llistar = comandes.add_parser("list", help="Mostra totes les tasques")
    llistar.add_argument(
        "--short",
        action="store_true",
        help="Mostra un resum de les tasques",
    )

    completar = comandes.add_parser("complete", help="Marca una tasca com a completada")
    completar.add_argument("--id", required=True, type=int, help="ID de la tasca")

    desfer = comandes.add_parser("undo", help="Marca una tasca com a pendent")
    desfer.add_argument("--id", required=True, type=int, help="ID de la tasca")

    eliminar = comandes.add_parser("delete", help="Elimina una tasca existent")
    eliminar.add_argument("--id", required=True, type=int, help="ID de la tasca")
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
            # ID inexistent -> ValueError -> stderr i codi 1 (GS-16)
            canviat = aplicar_estat(args.id, "completada")
            print(missatge_estat(args.id, "completada", canviat))
        elif args.comanda == "undo":
            # Comportament de v1: missatge per stdout i codi 0 (GS-08)
            print(canviar_estat(args.id, "pendent"))
        elif args.comanda == "delete":
            print(eliminar_tasca(args.id))
        else:
            linies = resum_tasques() if args.short else llistar_tasques()
            for linia in linies:
                print(linia)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
