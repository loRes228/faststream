from typing import Any

import pytest
from dirty_equals import IsInt, IsUUID
from opentelemetry.sdk.trace import Span
from opentelemetry.semconv.trace import SpanAttributes as SpanAttr
from opentelemetry.trace import SpanKind

from faststream.opentelemetry.consts import MESSAGING_DESTINATION_PUBLISH_NAME
from faststream.opentelemetry.middleware import MessageAction as Action
from faststream.rabbit import RabbitBroker, RabbitExchange
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware
from tests.brokers.rabbit.basic import RabbitTestcaseConfig
from tests.brokers.rabbit.test_consume import TestConsume as ConsumeCase
from tests.brokers.rabbit.test_publish import TestPublish as PublishCase
from tests.opentelemetry.basic import LocalTelemetryTestcase


@pytest.fixture()
def exchange(queue):
    return RabbitExchange(name=queue)


@pytest.mark.connected()
@pytest.mark.rabbit()
class TestTelemetry(RabbitTestcaseConfig, LocalTelemetryTestcase):  # type: ignore[misc]
    messaging_system = "rabbitmq"
    include_messages_counters = False
    telemetry_middleware_class = RabbitTelemetryMiddleware

    def destination_name(self, queue: str) -> str:
        return f"default.{queue}"

    def assert_span(
        self,
        span: Span,
        action: str,
        queue: str,
        msg: str,
        parent_span_id: str | None = None,
    ) -> None:
        attrs = span.attributes
        assert attrs[SpanAttr.MESSAGING_SYSTEM] == self.messaging_system
        assert attrs[SpanAttr.MESSAGING_MESSAGE_CONVERSATION_ID] == IsUUID
        assert attrs[SpanAttr.MESSAGING_RABBITMQ_DESTINATION_ROUTING_KEY] == queue
        assert span.name == f"{self.destination_name(queue)} {action}"
        assert span.kind in {SpanKind.CONSUMER, SpanKind.PRODUCER}

        if span.kind == SpanKind.PRODUCER and action in {Action.CREATE, Action.PUBLISH}:
            assert attrs[SpanAttr.MESSAGING_DESTINATION_NAME] == ""

        if span.kind == SpanKind.CONSUMER and action in {Action.CREATE, Action.PROCESS}:
            assert attrs[MESSAGING_DESTINATION_PUBLISH_NAME] == ""
            assert attrs["messaging.rabbitmq.message.delivery_tag"] == IsInt
            assert attrs[SpanAttr.MESSAGING_MESSAGE_ID] == IsUUID

        if action == Action.PROCESS:
            assert attrs[SpanAttr.MESSAGING_MESSAGE_PAYLOAD_SIZE_BYTES] == len(msg)
            assert attrs[SpanAttr.MESSAGING_OPERATION] == action

        if action == Action.PUBLISH:
            assert attrs[SpanAttr.MESSAGING_OPERATION] == action

        if parent_span_id:
            assert span.parent.span_id == parent_span_id


@pytest.mark.connected()
@pytest.mark.rabbit()
class TestPublishWithTelemetry(PublishCase):
    def get_broker(self, apply_types: bool = False, **kwargs: Any) -> RabbitBroker:
        return RabbitBroker(
            middlewares=(RabbitTelemetryMiddleware(),),
            apply_types=apply_types,
            **kwargs,
        )


@pytest.mark.connected()
@pytest.mark.rabbit()
class TestConsumeWithTelemetry(ConsumeCase):
    def get_broker(self, apply_types: bool = False, **kwargs: Any) -> RabbitBroker:
        return RabbitBroker(
            middlewares=(RabbitTelemetryMiddleware(),),
            apply_types=apply_types,
            **kwargs,
        )
