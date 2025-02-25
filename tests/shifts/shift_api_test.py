from fastapi.testclient import TestClient

from playground.core.models.shift import Shift
from playground.core.services.classes.repository_in_memory_chooser import InMemoryChooser
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository
from playground.runner.setup import setup, SetupConfiguration


def get_http(
    shift_repo: ShiftRepository = ShiftInMemoryRepository(),
) -> TestClient:
    return TestClient(
        setup(SetupConfiguration(repository_chooser=InMemoryChooser(shift_repo=shift_repo)))
    )
