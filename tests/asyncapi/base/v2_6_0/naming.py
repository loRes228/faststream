from typing import Any

from dirty_equals import Contains, HasLen, IsStr
from pydantic import create_model

from faststream._internal.broker import BrokerUsecase

from .basic import AsyncAPI260Factory


class BaseNaming(AsyncAPI260Factory):
    broker_class: type[BrokerUsecase[Any, Any]]


class SubscriberNaming(BaseNaming):
    def test_subscriber_naming(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test")
        async def handle_user_created(msg: str) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:HandleUserCreated"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:HandleUserCreated:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Message:Payload",
        ]

    def test_pydantic_subscriber_naming(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test")
        async def handle_user_created(msg: create_model("SimpleModel")) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:HandleUserCreated"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:HandleUserCreated:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == ["SimpleModel"]

    def test_multi_subscribers_naming(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test")
        @broker.subscriber("test2")
        async def handle_user_created(msg: str) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == Contains(
            IsStr(regex=r"test[\w:]*:HandleUserCreated"),
            IsStr(regex=r"test2[\w:]*:HandleUserCreated"),
        ) & HasLen(2)

        assert list(schema["components"]["messages"].keys()) == Contains(
            IsStr(regex=r"test[\w:]*:HandleUserCreated:Message"),
            IsStr(regex=r"test2[\w:]*:HandleUserCreated:Message"),
        ) & HasLen(2)

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Message:Payload",
        ]

    def test_subscriber_naming_manual(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test", title="custom")
        async def handle_user_created(msg: str) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "custom:Message:Payload",
        ]

    def test_subscriber_naming_default(self) -> None:
        broker = self.broker_class()

        sub = broker.subscriber("test")  # noqa: F841

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:Subscriber"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:Subscriber:Message"),
        ]

        for key, v in schema["components"]["schemas"].items():
            assert key == "Subscriber:Message:Payload"
            assert v == {"title": key}

    def test_subscriber_naming_default_with_title(self) -> None:
        broker = self.broker_class()

        sub = broker.subscriber("test", title="custom")  # noqa: F841

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "custom:Message:Payload",
        ]

        assert schema["components"]["schemas"]["custom:Message:Payload"] == {
            "title": "custom:Message:Payload",
        }

    def test_multi_subscribers_naming_default(self) -> None:
        broker = self.broker_class()

        @broker.subscriber("test")
        async def handle_user_created(msg: str) -> None: ...

        sub1 = broker.subscriber("test2")  # noqa: F841
        sub2 = broker.subscriber("test3")  # noqa: F841

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == Contains(
            IsStr(regex=r"test[\w:]*:HandleUserCreated"),
            IsStr(regex=r"test2[\w:]*:Subscriber"),
            IsStr(regex=r"test3[\w:]*:Subscriber"),
        ) & HasLen(3)

        assert list(schema["components"]["messages"].keys()) == Contains(
            IsStr(regex=r"test[\w:]*:HandleUserCreated:Message"),
            IsStr(regex=r"test2[\w:]*:Subscriber:Message"),
            IsStr(regex=r"test3[\w:]*:Subscriber:Message"),
        ) & HasLen(3)

        assert list(schema["components"]["schemas"].keys()) == Contains(
            "HandleUserCreated:Message:Payload",
            "Subscriber:Message:Payload",
        ) & HasLen(2)

        assert schema["components"]["schemas"]["Subscriber:Message:Payload"] == {
            "title": "Subscriber:Message:Payload",
        }


class FilterNaming(BaseNaming):
    def test_subscriber_filter_base(self) -> None:
        broker = self.broker_class()

        sub = broker.subscriber("test")

        @sub
        async def handle_user_created(msg: str) -> None: ...

        @sub
        async def handle_user_id(msg: int) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:\[HandleUserCreated,HandleUserId\]"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:\[HandleUserCreated,HandleUserId\]:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Message:Payload",
            "HandleUserId:Message:Payload",
        ]

    def test_subscriber_filter_pydantic(self) -> None:
        broker = self.broker_class()

        sub = broker.subscriber("test")

        @sub
        async def handle_user_created(msg: create_model("SimpleModel")) -> None: ...

        @sub
        async def handle_user_id(msg: int) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:\[HandleUserCreated,HandleUserId\]"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:\[HandleUserCreated,HandleUserId\]:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            "SimpleModel",
            "HandleUserId:Message:Payload",
        ]

    def test_subscriber_filter_with_title(self) -> None:
        broker = self.broker_class()

        sub = broker.subscriber("test", title="custom")

        @sub
        async def handle_user_created(msg: str) -> None: ...

        @sub
        async def handle_user_id(msg: int) -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Message:Payload",
            "HandleUserId:Message:Payload",
        ]


class PublisherNaming(BaseNaming):
    def test_publisher_naming_base(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test")
        async def handle_user_created() -> str: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [IsStr(regex=r"test[\w:]*:Publisher")]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message:Payload"),
        ]

    def test_publisher_naming_pydantic(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test")
        async def handle_user_created() -> create_model("SimpleModel"): ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [IsStr(regex=r"test[\w:]*:Publisher")]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            "SimpleModel",
        ]

    def test_publisher_manual_naming(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test", title="custom")
        async def handle_user_created() -> str: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "custom:Message:Payload",
        ]

    def test_publisher_with_schema_naming(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test", schema=str)
        async def handle_user_created() -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [IsStr(regex=r"test[\w:]*:Publisher")]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message:Payload"),
        ]

    def test_publisher_manual_naming_with_schema(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test", title="custom", schema=str)
        async def handle_user_created() -> None: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "custom:Message:Payload",
        ]

    def test_multi_publishers_naming(self) -> None:
        broker = self.broker_class()

        @broker.publisher("test")
        @broker.publisher("test2")
        async def handle_user_created() -> str: ...

        schema = self.get_spec(broker).to_jsonable()

        names = list(schema["channels"].keys())
        assert names == Contains(
            IsStr(regex=r"test2[\w:]*:Publisher"),
            IsStr(regex=r"test[\w:]*:Publisher"),
        ) & HasLen(2), names

        messages = list(schema["components"]["messages"].keys())
        assert messages == Contains(
            IsStr(regex=r"test2[\w:]*:Publisher:Message"),
            IsStr(regex=r"test[\w:]*:Publisher:Message"),
        ) & HasLen(2), messages

        payloads = list(schema["components"]["schemas"].keys())
        assert payloads == Contains(
            IsStr(regex=r"test2[\w:]*:Publisher:Message:Payload"),
            IsStr(regex=r"test[\w:]*:Publisher:Message:Payload"),
        ) & HasLen(2), payloads

    def test_multi_publisher_usages(self) -> None:
        broker = self.broker_class()

        pub = broker.publisher("test")

        @pub
        async def handle_user_created() -> str: ...

        @pub
        async def handle() -> int: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher"),
        ]

        assert list(schema["components"]["messages"].keys()) == [
            IsStr(regex=r"test[\w:]*:Publisher:Message"),
        ]

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Publisher:Message:Payload",
            "Handle:Publisher:Message:Payload",
        ]

    def test_multi_publisher_usages_with_custom(self) -> None:
        broker = self.broker_class()

        pub = broker.publisher("test", title="custom")

        @pub
        async def handle_user_created() -> str: ...

        @pub
        async def handle() -> int: ...

        schema = self.get_spec(broker).to_jsonable()

        assert list(schema["channels"].keys()) == ["custom"]

        assert list(schema["components"]["messages"].keys()) == ["custom:Message"]

        assert list(schema["components"]["schemas"].keys()) == [
            "HandleUserCreated:Publisher:Message:Payload",
            "Handle:Publisher:Message:Payload",
        ]


class NamingTestCase(SubscriberNaming, FilterNaming, PublisherNaming):
    pass
