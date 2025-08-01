import pytest

from tests.marks import (
    require_aiokafka,
    require_aiopika,
    require_confluent,
    require_nats,
    require_redis,
)


@pytest.mark.kafka()
@pytest.mark.connected()
@pytest.mark.asyncio()
@require_aiokafka
async def test_handle_kafka() -> None:
    from docs.docs_src.getting_started.subscription.kafka.testing import (
        test_handle as test_handle_k,
    )

    await test_handle_k()


@pytest.mark.kafka()
@pytest.mark.connected()
@pytest.mark.asyncio()
@require_aiokafka
async def test_validate_kafka() -> None:
    from docs.docs_src.getting_started.subscription.kafka.testing import (
        test_validation_error as test_validation_error_k,
    )

    await test_validation_error_k()


@pytest.mark.connected()
@pytest.mark.confluent()
@pytest.mark.asyncio()
@require_confluent
async def test_handle_confluent() -> None:
    from docs.docs_src.getting_started.subscription.confluent.testing import (
        test_handle as test_handle_confluent,
    )

    await test_handle_confluent()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.confluent()
@require_confluent
async def test_validate_confluent() -> None:
    from docs.docs_src.getting_started.subscription.confluent.testing import (
        test_validation_error as test_validation_error_confluent,
    )

    await test_validation_error_confluent()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.rabbit()
@require_aiopika
async def test_handle_rabbit() -> None:
    from docs.docs_src.getting_started.subscription.rabbit.testing import (
        test_handle as test_handle_r,
    )

    await test_handle_r()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.rabbit()
@require_aiopika
async def test_validate_rabbit() -> None:
    from docs.docs_src.getting_started.subscription.rabbit.testing import (
        test_validation_error as test_validation_error_r,
    )

    await test_validation_error_r()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.nats()
@require_nats
async def test_handle_nats() -> None:
    from docs.docs_src.getting_started.subscription.nats.testing import (
        test_handle as test_handle_n,
    )

    await test_handle_n()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.nats()
@require_nats
async def test_validate_nats() -> None:
    from docs.docs_src.getting_started.subscription.nats.testing import (
        test_validation_error as test_validation_error_n,
    )

    await test_validation_error_n()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.redis()
@require_redis
async def test_handle_redis() -> None:
    from docs.docs_src.getting_started.subscription.redis.testing import (
        test_handle as test_handle_rd,
    )

    await test_handle_rd()


@pytest.mark.connected()
@pytest.mark.asyncio()
@pytest.mark.redis()
@require_redis
async def test_validate_redis() -> None:
    from docs.docs_src.getting_started.subscription.redis.testing import (
        test_validation_error as test_validation_error_rd,
    )

    await test_validation_error_rd()
