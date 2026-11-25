import json
from dataclasses import dataclass
from typing import Any


@dataclass(init=False)
class Task:
    id: int
    titol: str
    assignatura: str
    estat: str

    def __init__(
        self,
        id: int,
        titol: str | None = None,
        assignatura: str | None = None,
        estat: str = "pendent",
        *,
        title: str | None = None,
        subject: str | None = None,
        status: str | None = None,
    ) -> None:
        self.id = int(id)
        self.titol = str(titol if titol is not None else (title or ""))
        self.assignatura = str(
            assignatura if assignatura is not None else (subject or "")
        )
        self.estat = str(status if status is not None else estat)

    @property
    def title(self) -> str:
        return self.titol

    @property
    def subject(self) -> str:
        return self.assignatura

    @property
    def status(self) -> str:
        return self.estat

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.titol,
            "subject": self.assignatura,
            "status": self.estat,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            titol=data.get("titol", data.get("títol", data.get("title"))),
            assignatura=data.get("assignatura", data.get("subject")),
            estat=data.get("estat", data.get("status", "pendent")),
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
