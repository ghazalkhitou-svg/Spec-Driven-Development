import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any


PATRO_DATA_LIMIT = re.compile(r"\d{4}-\d{2}-\d{2}")
MISSATGE_DATA_INVALIDA = "La data límit és incorrecta. Format esperat: YYYY-MM-DD."


def validar_data_limit(valor: str | None) -> None:
    if valor is None:
        return
    if not isinstance(valor, str) or not PATRO_DATA_LIMIT.fullmatch(valor):
        raise ValueError(MISSATGE_DATA_INVALIDA)
    try:
        date.fromisoformat(valor)
    except ValueError as error:
        raise ValueError(MISSATGE_DATA_INVALIDA) from error


@dataclass(init=False)
class Task:
    id: int
    titol: str
    assignatura: str
    estat: str
    data_limit: str | None

    def __init__(
        self,
        id: int,
        titol: str | None = None,
        assignatura: str | None = None,
        estat: str = "pendent",
        data_limit: str | None = None,
        *,
        title: str | None = None,
        subject: str | None = None,
        status: str | None = None,
        due: str | None = None,
    ) -> None:
        self.id = int(id)
        self.titol = str(titol if titol is not None else (title or ""))
        self.assignatura = str(
            assignatura if assignatura is not None else (subject or "")
        )
        self.estat = str(status if status is not None else estat)
        data_final = due if due is not None else data_limit
        self.data_limit = str(data_final) if data_final is not None else None

    @property
    def title(self) -> str:
        return self.titol

    @property
    def subject(self) -> str:
        return self.assignatura

    @property
    def status(self) -> str:
        return self.estat

    @property
    def due(self) -> str | None:
        return self.data_limit

    def to_dict(self) -> dict[str, Any]:
        resultat: dict[str, Any] = {
            "id": self.id,
            "title": self.titol,
            "subject": self.assignatura,
            "status": self.estat,
        }
        if self.data_limit is not None:
            resultat["due"] = self.data_limit
        return resultat

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            titol=data.get("titol", data.get("títol", data.get("title"))),
            assignatura=data.get("assignatura", data.get("subject")),
            estat=data.get("estat", data.get("status", "pendent")),
            data_limit=data.get("due", data.get("data_limit")),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, value: str) -> "Task":
        return cls.from_dict(json.loads(value))


def tasks_to_json(tasques: list[Task]) -> str:
    return json.dumps(
        [tasca.to_dict() for tasca in tasques],
        ensure_ascii=False,
        indent=2,
    )


def tasks_from_json(value: str) -> list[Task]:
    return [Task.from_dict(item) for item in json.loads(value)]
