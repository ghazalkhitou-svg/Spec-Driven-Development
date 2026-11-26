import json
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest


RUTA_ARREL = Path(__file__).resolve().parent.parent


@pytest.fixture
def projecte_temporal(tmp_path: Path) -> Path:
    projecte = tmp_path / "projecte"
    shutil.copytree(
        RUTA_ARREL / "src",
        projecte / "src",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    return projecte


def executar(
    projecte: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(projecte / "src" / "tasks_app.py"), *args],
        cwd=projecte,
        capture_output=True,
        text=True,
        check=check,
    )


TASQUES_INICIALS = [
    {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
    {"id": 2, "title": "Examen parcial", "subject": "SO", "status": "pendent"},
]


def escriure_tasques(projecte: Path, tasques: list[dict[str, object]]) -> None:
    fitxer = projecte / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(json.dumps(tasques, ensure_ascii=False), encoding="utf-8")


def tasques_desades(projecte: Path) -> list[dict[str, object]]:
    fitxer = projecte / "data" / "tasks.json"
    return json.loads(fitxer.read_text(encoding="utf-8"))


def test_gs01_creacio_correcta_duna_tasca(projecte_temporal: Path) -> None:
    resultat = executar(
        projecte_temporal,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
    )

    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    fitxer = projecte_temporal / "data" / "tasks.json"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {
            "id": 1,
            "title": "Pràctica 1",
            "subject": "RS",
            "status": "pendent",
        }
    ]


def test_gs02_llistat_buit(projecte_temporal: Path) -> None:
    resultat = executar(projecte_temporal, "list")

    assert resultat.stdout.strip() == "Registre de tasques buit."
    fitxer = projecte_temporal / "data" / "tasks.json"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == []


def test_gs03_llistat_amb_registres(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "title": "Pràctica 1",
                    "subject": "RS",
                    "status": "pendent",
                },
                {
                    "id": 2,
                    "title": "Examen parcial",
                    "subject": "SO",
                    "status": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar(projecte_temporal, "list")

    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]


def test_gs04_marcar_tasca_completada(projecte_temporal: Path) -> None:
    tasques = [dict(tasca) for tasca in TASQUES_INICIALS]
    escriure_tasques(projecte_temporal, tasques)

    resultat = executar(projecte_temporal, "complete", "--id", "1")

    assert resultat.stdout.strip() == "Tasca [ID: 1] completada amb èxit"
    assert [tasca["status"] for tasca in tasques_desades(projecte_temporal)] == [
        "completada",
        "pendent",
    ]


def test_gs05_marcar_tasca_pendent(projecte_temporal: Path) -> None:
    tasques = [dict(tasca) for tasca in TASQUES_INICIALS]
    tasques[0]["status"] = "completada"
    escriure_tasques(projecte_temporal, tasques)

    resultat = executar(projecte_temporal, "undo", "--id", "1")

    assert resultat.stdout.strip() == "Tasca [ID: 1] marcada com a pendent"
    assert [tasca["status"] for tasca in tasques_desades(projecte_temporal)] == [
        "pendent",
        "pendent",
    ]


def test_gs06_completar_tasca_ja_completada(projecte_temporal: Path) -> None:
    tasques = [dict(tasca) for tasca in TASQUES_INICIALS]
    tasques[0]["status"] = "completada"
    escriure_tasques(projecte_temporal, tasques)

    resultat = executar(projecte_temporal, "complete", "--id", "1")

    assert resultat.stdout.strip() == (
        "Tasca [ID: 1] ja està marcada com a completada"
    )
    assert tasques_desades(projecte_temporal) == tasques


def test_gs07_desfer_tasca_ja_pendent(projecte_temporal: Path) -> None:
    escriure_tasques(projecte_temporal, TASQUES_INICIALS)

    resultat = executar(projecte_temporal, "undo", "--id", "1")

    assert resultat.stdout.strip() == "Tasca [ID: 1] ja està marcada com a pendent"
    assert tasques_desades(projecte_temporal) == TASQUES_INICIALS


@pytest.mark.parametrize("comanda", ["undo"])
def test_gs08_canviar_estat_tasca_inexistent(
    projecte_temporal: Path, comanda: str
) -> None:
    escriure_tasques(projecte_temporal, TASQUES_INICIALS)

    resultat = executar(projecte_temporal, comanda, "--id", "99")

    assert resultat.stdout.strip() == "Tasca [ID: 99] no existeix"
    assert tasques_desades(projecte_temporal) == TASQUES_INICIALS


def test_gs09_eliminar_tasca_existent(projecte_temporal: Path) -> None:
    escriure_tasques(projecte_temporal, TASQUES_INICIALS)

    resultat = executar(projecte_temporal, "delete", "--id", "1")

    assert resultat.stdout.strip() == "Tasca [ID: 1] eliminada amb èxit"
    assert tasques_desades(projecte_temporal) == [TASQUES_INICIALS[1]]


def test_gs10_eliminar_tasca_inexistent(projecte_temporal: Path) -> None:
    escriure_tasques(projecte_temporal, TASQUES_INICIALS)

    resultat = executar(projecte_temporal, "delete", "--id", "99")

    assert resultat.stdout.strip() == "Tasca [ID: 99] no existeix"
    assert tasques_desades(projecte_temporal) == TASQUES_INICIALS


def test_gs11_alta_amb_data_limit(projecte_temporal: Path) -> None:
    resultat = executar(
        projecte_temporal,
        "add",
        "--title",
        "Pràctica 2",
        "--subject",
        "RS",
        "--due",
        "2026-12-02",
    )

    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    fitxer = projecte_temporal / "data" / "tasks.json"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {
            "id": 1,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": "2026-12-02",
        }
    ]


@pytest.mark.parametrize(
    "data",
    ["2026-2-03", "2026-02-30", "02/12/2026"],
)
def test_gs12_data_limit_incorrecta_no_modifica_registre(
    projecte_temporal: Path,
    data: str,
) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    registre_original = [
        {
            "id": 1,
            "title": "Pràctica 1",
            "subject": "RS",
            "status": "pendent",
        }
    ]
    contingut_original = json.dumps(registre_original, ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "add",
        "--title",
        "Prova",
        "--subject",
        "RS",
        "--due",
        data,
        check=False,
    )

    assert resultat.returncode != 0
    assert "data límit" in resultat.stderr
    assert fitxer.read_text(encoding="utf-8") == contingut_original
    assert json.loads(fitxer.read_text(encoding="utf-8")) == registre_original


def test_gs21_compatibilitat_amb_registre_v1(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    tasca_v1 = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }
    fitxer.write_text(json.dumps([tasca_v1], ensure_ascii=False), encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "add",
        "--title",
        "Pràctica 2",
        "--subject",
        "SO",
    )

    assert resultat.stdout.strip() == "Tasca [ID: 2] creada amb èxit"
    dades = json.loads(fitxer.read_text(encoding="utf-8"))
    assert dades[0] == tasca_v1
    assert dades[1] == {
        "id": 2,
        "title": "Pràctica 2",
        "subject": "SO",
        "status": "pendent",
    }
    assert "due" not in dades[1]

    llistat = executar(projecte_temporal, "list")
    assert llistat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Pràctica 2 (SO) - estat: pendent",
    ]


def test_gs13_edicio_parcial(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
        "due": "2026-12-02",
    }
    fitxer.write_text(json.dumps([original], ensure_ascii=False), encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "edit",
        "--id",
        "1",
        "--title",
        "Pràctica revisada",
    )

    assert resultat.stdout.strip() == "Tasca [ID: 1] modificada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {**original, "title": "Pràctica revisada"}
    ]


def test_gs14_edicio_de_diversos_atributs(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "title": "Pràctica 1",
                    "subject": "RS",
                    "status": "pendent",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar(
        projecte_temporal,
        "edit",
        "--id",
        "1",
        "--title",
        "Examen final",
        "--subject",
        "SO",
        "--due",
        "2026-12-15",
        "--status",
        "completada",
    )

    esperat = {
        "id": 1,
        "title": "Examen final",
        "subject": "SO",
        "status": "completada",
        "due": "2026-12-15",
    }
    assert resultat.stdout.strip() == "Tasca [ID: 1] modificada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [esperat]

    llistat = executar(projecte_temporal, "list")
    assert llistat.stdout.splitlines() == [
        "[1] Examen final (SO) - estat: completada - data límit: 2026-12-15"
    ]


def test_gs16_id_inexistent_en_edit(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }
    contingut_original = json.dumps([original], ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "edit",
        "--id",
        "99",
        "--title",
        "Prova",
        check=False,
    )

    assert resultat.returncode != 0
    assert "ID 99" in resultat.stderr
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs19_edicio_amb_data_incorrecta(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Original",
        "subject": "RS",
        "status": "pendent",
        "due": "2026-12-02",
    }
    contingut_original = json.dumps([original], ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "edit",
        "--id",
        "1",
        "--title",
        "Nou",
        "--due",
        "2026-02-30",
        check=False,
    )

    assert resultat.returncode != 0
    assert "data límit" in resultat.stderr
    assert fitxer.read_text(encoding="utf-8") == contingut_original
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [original]


@pytest.mark.parametrize(
    ("arguments", "missatge"),
    [
        (("edit", "--id", "1"), "almenys un atribut"),
        (("edit", "--id", "1", "--status", "desconegut"), "estat"),
    ],
)
def test_gs20_edicio_sense_atributs_o_estat_invalid(
    projecte_temporal: Path,
    arguments: tuple[str, ...],
    missatge: str,
) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }
    contingut_original = json.dumps([original], ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(projecte_temporal, *arguments, check=False)

    assert resultat.returncode != 0
    assert missatge in resultat.stderr
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs15_complecio_duna_tasca(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Pràctica 2",
        "subject": "RS",
        "status": "pendent",
        "due": "2026-12-02",
    }
    fitxer.write_text(json.dumps([original], ensure_ascii=False), encoding="utf-8")

    resultat = executar(projecte_temporal, "complete", "--id", "1")

    esperat = {**original, "status": "completada"}
    assert resultat.stdout.strip() == "Tasca [ID: 1] completada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [esperat]

    repeticio = executar(projecte_temporal, "complete", "--id", "1")

    assert repeticio.stdout.strip() == (
        "Tasca [ID: 1] ja està marcada com a completada"
    )
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [esperat]


def test_gs16_id_inexistent_en_complete(projecte_temporal: Path) -> None:
    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    original = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }
    contingut_original = json.dumps([original], ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(
        projecte_temporal,
        "complete",
        "--id",
        "99",
        check=False,
    )

    assert resultat.returncode != 0
    assert "ID 99" in resultat.stderr
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs17_llistat_caducades_i_urgents(projecte_temporal: Path) -> None:
    avui = date.today()
    desplaçaments = (-1, 0, 1, 6, 7, 8)
    etiquetes = ("[CADUCADA]", "[URGENT]", "[URGENT]", "[URGENT]", None, None)
    tasques = []
    esperades = []

    for id_tasca, (dies, etiqueta) in enumerate(
        zip(desplaçaments, etiquetes),
        start=1,
    ):
        data_limit = (avui + timedelta(days=dies)).isoformat()
        tasques.append(
            {
                "id": id_tasca,
                "title": f"Tasca {id_tasca}",
                "subject": "RS",
                "status": "pendent",
                "due": data_limit,
            }
        )
        linia = (
            f"[{id_tasca}] Tasca {id_tasca} (RS) - estat: pendent"
            f" - data límit: {data_limit}"
        )
        if etiqueta is not None:
            linia += f" {etiqueta}"
        esperades.append(linia)

    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    contingut_original = json.dumps(tasques, ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(projecte_temporal, "list")

    assert resultat.stdout.splitlines() == esperades
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs18_tasques_sense_etiqueta_temporal(projecte_temporal: Path) -> None:
    avui = date.today()
    data_passada = (avui - timedelta(days=1)).isoformat()
    data_proxima = (avui + timedelta(days=1)).isoformat()
    registre = [
        {
            "id": 1,
            "title": "Completada passada",
            "subject": "RS",
            "status": "completada",
            "due": data_passada,
        },
        {
            "id": 2,
            "title": "Completada pròxima",
            "subject": "SO",
            "status": "completada",
            "due": data_proxima,
        },
        {
            "id": 3,
            "title": "Sense data",
            "subject": "RS",
            "status": "pendent",
        },
    ]

    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    contingut_original = json.dumps(registre, ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(projecte_temporal, "list")

    assert resultat.stdout.splitlines() == [
        f"[1] Completada passada (RS) - estat: completada"
        f" - data límit: {data_passada}",
        f"[2] Completada pròxima (SO) - estat: completada"
        f" - data límit: {data_proxima}",
        "[3] Sense data (RS) - estat: pendent",
    ]
    assert "[CADUCADA]" not in resultat.stdout
    assert "[URGENT]" not in resultat.stdout
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs22_format_llistat_amb_data_limit(projecte_temporal: Path) -> None:
    avui = date.today()
    data_limit = (avui + timedelta(days=1)).isoformat()
    registre = [
        {
            "id": 1,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": data_limit,
        }
    ]

    fitxer = projecte_temporal / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    contingut_original = json.dumps(registre, ensure_ascii=False)
    fitxer.write_text(contingut_original, encoding="utf-8")

    resultat = executar(projecte_temporal, "list")

    assert resultat.stdout.strip() == (
        f"[1] Pràctica 2 (RS) - estat: pendent"
        f" - data límit: {data_limit} [URGENT]"
    )
    assert fitxer.read_text(encoding="utf-8") == contingut_original


def test_gs23_resum_de_les_tasques(projecte_temporal: Path) -> None:
    avui = date.today()
    registre = [
        {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
        {"id": 2, "title": "Examen parcial", "subject": "SO", "status": "pendent"},
        {
            "id": 3,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": (avui - timedelta(days=1)).isoformat(),
        },
        {
            "id": 4,
            "title": "Examen parcial 2",
            "subject": "SO",
            "status": "pendent",
            "due": (avui - timedelta(days=2)).isoformat(),
        },
        {
            "id": 5,
            "title": "Pràctica 3",
            "subject": "RS",
            "status": "pendent",
            "due": (avui + timedelta(days=1)).isoformat(),
        },
        {
            "id": 6,
            "title": "Examen final",
            "subject": "SO",
            "status": "completada",
        },
    ]
    escriure_tasques(projecte_temporal, registre)

    resultat = executar(projecte_temporal, "list", "--short")

    assert resultat.stdout.splitlines() == [
        "Nombre total de tasques: 6",
        "Nombre total de tasques pendents: 2",
        "Nombre total de tasques completades: 1",
        "Nombre total de tasques urgents: 1",
        "Nombre total de tasques caducades: 2",
    ]


def test_gs24_filtratge_per_assignatura_amb_tasques(
    projecte_temporal: Path,
) -> None:
    avui = date.today()
    data_caducada = (avui - timedelta(days=1)).isoformat()
    data_urgent = (avui + timedelta(days=1)).isoformat()
    registre = [
        {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
        {"id": 2, "title": "Examen parcial", "subject": "SO", "status": "pendent"},
        {
            "id": 3,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": data_caducada,
        },
        {
            "id": 4,
            "title": "Examen parcial 2",
            "subject": "SO",
            "status": "pendent",
            "due": (avui - timedelta(days=2)).isoformat(),
        },
        {
            "id": 5,
            "title": "Pràctica 3",
            "subject": "RS",
            "status": "pendent",
            "due": data_urgent,
        },
    ]
    escriure_tasques(projecte_temporal, registre)

    resultat = executar(projecte_temporal, "list", "--subject", "RS")

    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        f"[3] Pràctica 2 (RS) - estat: pendent"
        f" - data límit: {data_caducada} [CADUCADA]",
        f"[5] Pràctica 3 (RS) - estat: pendent"
        f" - data límit: {data_urgent} [URGENT]",
    ]
    assert tasques_desades(projecte_temporal) == registre


def test_gs25_filtratge_per_assignatura_sense_tasques(
    projecte_temporal: Path,
) -> None:
    avui = date.today()
    registre = [
        {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
        {
            "id": 2,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": (avui - timedelta(days=1)).isoformat(),
        },
        {
            "id": 3,
            "title": "Pràctica 3",
            "subject": "RS",
            "status": "pendent",
            "due": (avui + timedelta(days=1)).isoformat(),
        },
    ]
    escriure_tasques(projecte_temporal, registre)

    resultat = executar(projecte_temporal, "list", "--subject", "SO")

    assert resultat.stdout.strip() == "No hi ha cap tasca d'aquesta assignatura"
    assert tasques_desades(projecte_temporal) == registre


def test_gs26_filtratge_per_paraula_clau(projecte_temporal: Path) -> None:
    avui = date.today()
    data_caducada = (avui - timedelta(days=1)).isoformat()
    data_urgent = (avui + timedelta(days=1)).isoformat()
    registre = [
        {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
        {"id": 2, "title": "Examen parcial", "subject": "SO", "status": "pendent"},
        {
            "id": 3,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": data_caducada,
        },
        {
            "id": 4,
            "title": "Examen parcial 2",
            "subject": "SO",
            "status": "pendent",
            "due": (avui - timedelta(days=2)).isoformat(),
        },
        {
            "id": 5,
            "title": "Pràctica 3",
            "subject": "RS",
            "status": "pendent",
            "due": data_urgent,
        },
    ]
    escriure_tasques(projecte_temporal, registre)

    resultat = executar(projecte_temporal, "list", "--find", "ctica")

    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        f"[3] Pràctica 2 (RS) - estat: pendent"
        f" - data límit: {data_caducada} [CADUCADA]",
        f"[5] Pràctica 3 (RS) - estat: pendent"
        f" - data límit: {data_urgent} [URGENT]",
    ]
    assert tasques_desades(projecte_temporal) == registre


def test_gs27_filtratge_per_paraula_clau_sense_resultats(
    projecte_temporal: Path,
) -> None:
    avui = date.today()
    registre = [
        {"id": 1, "title": "Pràctica 1", "subject": "RS", "status": "pendent"},
        {"id": 2, "title": "Examen parcial", "subject": "SO", "status": "pendent"},
        {
            "id": 3,
            "title": "Pràctica 2",
            "subject": "RS",
            "status": "pendent",
            "due": (avui - timedelta(days=1)).isoformat(),
        },
        {
            "id": 4,
            "title": "Examen parcial 2",
            "subject": "SO",
            "status": "pendent",
            "due": (avui - timedelta(days=2)).isoformat(),
        },
        {
            "id": 5,
            "title": "Pràctica 3",
            "subject": "RS",
            "status": "pendent",
            "due": (avui + timedelta(days=1)).isoformat(),
        },
    ]
    escriure_tasques(projecte_temporal, registre)

    resultat = executar(projecte_temporal, "list", "--find", "wwww")

    assert resultat.stdout.strip() == "Cap tasca conté wwww en el seu títol"
    assert tasques_desades(projecte_temporal) == registre