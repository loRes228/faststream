import pytest

from faststream import TestApp
from faststream.nats import TestNatsBroker


@pytest.mark.nats()
@pytest.mark.asyncio()
async def test_basic() -> None:
    from examples.nats.e02_basic_rpc import app, broker, handler

    async with TestNatsBroker(broker), TestApp(app):
        handler.mock.assert_called_once_with("Hi!")
