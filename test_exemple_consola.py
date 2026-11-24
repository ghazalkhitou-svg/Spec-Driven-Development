import subprocess
import sys
from pathlib import Path

import pytest


PROGRAM = Path(__file__).with_name("exemple_consola.py")
MISSATGE_ERROR = "Crida incorrecta. Utilitza 'exemple_consola [valor entre 1 i 9]"


def executar(*args):
    resultat = subprocess.run(
        [sys.executable, str(PROGRAM), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return resultat


def test_fitxer_programa_existeix():
    assert PROGRAM.is_file()


@pytest.mark.parametrize("arguments", [(), ("0",), ("10",), ("a",), ("1.5",), ("-1",), ("01",), ("1", "2")])
def test_crida_incorrecta(arguments):
    resultat = executar(*arguments)
    assert resultat.stdout.strip() == MISSATGE_ERROR
    assert resultat.stderr == ""
    assert resultat.returncode == 0


@pytest.mark.parametrize("digit", "123456789")
def test_sortida_correcta(digit):
    resultat = executar(digit)
    esperat = "\n".join([digit * int(digit)] * int(digit))
    assert resultat.stdout.strip() == esperat
    assert resultat.stderr == ""
    assert resultat.returncode == 0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
