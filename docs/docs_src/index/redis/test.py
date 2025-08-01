from .pydantic import broker

import pytest
from pydantic import ValidationError
from faststream.redis import TestRedisBroker


@pytest.mark.asyncio
async def test_correct() -> None:
    async with TestRedisBroker(broker) as br:
        await br.publish(
            {
                "user": "John",
                "user_id": 1,
            }, "in-channel",
        )

@pytest.mark.asyncio
async def test_invalid() -> None:
    async with TestRedisBroker(broker) as br:
        with pytest.raises(ValidationError):
            await br.publish("wrong message", "in-channel")
