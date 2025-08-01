import pytest

from faststream.rabbit import TestApp, TestRabbitBroker


@pytest.mark.rabbit()
@pytest.mark.asyncio()
async def test_index() -> None:
    from examples.rabbit.direct import (
        app,
        base_handler1,
        base_handler3,
        broker,
    )

    async with TestRabbitBroker(broker), TestApp(app):
        base_handler1.mock.assert_called_with(b"")
        base_handler3.mock.assert_called_once_with(b"")
