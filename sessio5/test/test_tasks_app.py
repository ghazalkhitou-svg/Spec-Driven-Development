import json
import shutil
import subprocess
import sys
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


def executar(projecte: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(projecte / "src" / "tasks_app.py"), *args],
        cwd=projecte,
        capture_output=True,
        text=True,
        check=True,
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

    assert resultat.stdout.strip() == "Tasca [ID: 1] marcada com a completada"
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


@pytest.mark.parametrize("comanda", ["complete", "undo"])
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
