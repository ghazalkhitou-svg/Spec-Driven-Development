import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from models import Task, tasks_from_json, tasks_to_json


def test_serialitzacio_amb_data_limit() -> None:
    tasca = Task(1, "Pràctica 2", "RS", data_limit="2026-12-02")
    esperat = {
        "id": 1,
        "title": "Pràctica 2",
        "subject": "RS",
        "status": "pendent",
        "due": "2026-12-02",
    }

    assert tasca.due == "2026-12-02"
    assert tasca.to_dict() == esperat
    assert json.loads(tasca.to_json()) == esperat
    assert Task.from_dict(esperat) == tasca
    assert Task.from_json(tasca.to_json()) == tasca
    assert Task(id=2, title="Prova", subject="RS", due="2026-12-15").data_limit == (
        "2026-12-15"
    )


def test_serialitzacio_sense_data_limit() -> None:
    tasca = Task(1, "Pràctica 1", "RS")
    esperat = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }

    assert tasca.data_limit is None
    assert tasca.to_dict() == esperat
    assert "due" not in tasca.to_dict()
    assert json.loads(tasca.to_json()) == esperat
    assert Task.from_json(tasca.to_json()) == tasca


def test_lectura_de_registre_antic_sense_data_limit() -> None:
    antic = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }

    tasca = Task.from_dict(antic)

    assert tasca.data_limit is None
    assert tasca.to_dict() == antic
    assert tasks_from_json(json.dumps([antic])) == [tasca]
    assert json.loads(tasks_to_json([tasca])) == [antic]


def test_lectura_de_registre_antic_amb_claus_alternatives() -> None:
    antic = {
        "id": 2,
        "títol": "Examen",
        "assignatura": "SO",
        "estat": "pendent",
    }

    tasca = Task.from_dict(antic)

    assert tasca.titol == "Examen"
    assert tasca.assignatura == "SO"
    assert tasca.estat == "pendent"
    assert tasca.data_limit is None
    assert tasca.to_dict() == {
        "id": 2,
        "title": "Examen",
        "subject": "SO",
        "status": "pendent",
    }


def test_serialitzacio_de_llista_amb_i_sense_data_limit() -> None:
    antigues = {
        "id": 1,
        "title": "Pràctica 1",
        "subject": "RS",
        "status": "pendent",
    }
    nova = {
        "id": 2,
        "title": "Pràctica 2",
        "subject": "RS",
        "status": "pendent",
        "due": "2026-12-02",
    }

    serialized = tasks_to_json([Task.from_dict(antigues), Task.from_dict(nova)])

    assert json.loads(serialized) == [antigues, nova]
    assert tasks_from_json(serialized) == [
        Task.from_dict(antigues),
        Task.from_dict(nova),
    ]
