import pytest

from faststream.nats import NatsBroker
from tests.asyncapi.base.v3_0_0.naming import NamingTestCase


@pytest.mark.nats()
class TestNaming(NamingTestCase):
    broker_class = NatsBroker

    def test_base(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test")
        async def handle() -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert schema == {
            "asyncapi": "3.0.0",
            "defaultContentType": "application/json",
            "info": {"title": "FastStream", "version": "0.1.0"},
            "servers": {
                "development": {
                    "host": "localhost:4222",
                    "pathname": "",
                    "protocol": "nats",
                    "protocolVersion": "custom",
                },
            },
            "channels": {
                "test:Handle": {
                    "address": "test:Handle",
                    "servers": [
                        {
                            "$ref": "#/servers/development",
                        },
                    ],
                    "bindings": {
                        "nats": {"subject": "test", "bindingVersion": "custom"},
                    },
                    "messages": {
                        "SubscribeMessage": {
                            "$ref": "#/components/messages/test:Handle:SubscribeMessage",
                        },
                    },
                },
            },
            "operations": {
                "test:HandleSubscribe": {
                    "action": "receive",
                    "channel": {
                        "$ref": "#/channels/test:Handle",
                    },
                    "messages": [
                        {
                            "$ref": "#/channels/test:Handle/messages/SubscribeMessage",
                        },
                    ],
                },
            },
            "components": {
                "messages": {
                    "test:Handle:SubscribeMessage": {
                        "title": "test:Handle:SubscribeMessage",
                        "correlationId": {
                            "location": "$message.header#/correlation_id",
                        },
                        "payload": {"$ref": "#/components/schemas/EmptyPayload"},
                    },
                },
                "schemas": {"EmptyPayload": {"title": "EmptyPayload", "type": "null"}},
            },
        }
