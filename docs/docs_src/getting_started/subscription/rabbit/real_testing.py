import pytest
from pydantic import ValidationError

from faststream.rabbit import TestRabbitBroker

from .pydantic_fields import broker, handle


@pytest.mark.asyncio
async def test_handle() -> None:
    async with TestRabbitBroker(broker, with_real=True) as br:
        await br.publish({"name": "John", "user_id": 1}, queue="test-queue")
        await handle.wait_call(timeout=3)
        handle.mock.assert_called_once_with({"name": "John", "user_id": 1})

    assert not handle.mock.called  # mock is reset

@pytest.mark.asyncio
async def test_validation_error() -> None:
    async with TestRabbitBroker(broker, with_real=True) as br:
        with pytest.raises(ValidationError):
            await br.publish("wrong message", queue="test-queue")
            await handle.wait_call(timeout=3)

        handle.mock.assert_called_once_with("wrong message")
