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


def test_gs04_alta_amb_data_limit(projecte_temporal: Path) -> None:
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
def test_gs05_data_limit_incorrecta_no_modifica_registre(
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


def test_gs14_compatibilitat_amb_registre_v1(projecte_temporal: Path) -> None:
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


def test_gs06_edicio_parcial(projecte_temporal: Path) -> None:
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


def test_gs07_edicio_de_diversos_atributs(projecte_temporal: Path) -> None:
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
    assert llistat.stdout.splitlines() == ["[1] Examen final (SO) - estat: completada"]


def test_gs09_id_inexistent_en_edit(projecte_temporal: Path) -> None:
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


def test_gs12_edicio_amb_data_incorrecta(projecte_temporal: Path) -> None:
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
def test_gs13_edicio_sense_atributs_o_estat_invalid(
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
