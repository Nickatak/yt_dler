import pathlib
import sys

import pytest

# Unfortunately, this needs to happen first.
test_dir = pathlib.Path(__file__).parent

sys.path.append(str(test_dir.parent.absolute()))

from app import create_app  # noqa: E402
from conf import TestConf  # noqa: E402


@pytest.fixture
def app():
    yield create_app(TestConf)


@pytest.fixture()
def client(app):
    return app.test_client()
