from src.dependency_injection import di as di_module
from src.configuration.config import AppConfig


def test_get_configuration_singleton() -> None:
    # calling twice returns the same object
    c1 = di_module.get_configuration()
    c2 = di_module.get_configuration()
    assert c1 is c2

def test_get_engine_singleton() -> None:
    # ensure engine singleton behavior; reset global engine for test isolation
    prev = getattr(di_module, "engine", None)
    di_module.engine = None
    class DummyConfig(AppConfig):
        connection_string = "sqlite:///:memory:"

    try:
        e1 = di_module.get_engine(DummyConfig())
        e2 = di_module.get_engine(DummyConfig())
        assert e1 is e2
    finally:
        di_module.engine = prev
