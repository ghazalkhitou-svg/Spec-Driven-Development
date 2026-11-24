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
