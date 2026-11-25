from __future__ import annotations
from abc import ABC, abstractmethod
from payment import RzpChannelBuilder, StripeChannelBuilder


class GatewayBase(ABC):
    def __init__(self, label: str, fee_pct: float):
        self.label = label
        self.fee_pct = fee_pct

    @abstractmethod
    def dispatch(self, mode: str, amt: float, **creds) -> bool:
        pass


class RzpGateway(GatewayBase):
    def __init__(self):
        super().__init__("Razorpay", 2.0)

    def dispatch(self, mode: str, amt: float, **creds) -> bool:
        channel = RzpChannelBuilder.make_channel(mode, **creds)
        fee = round(amt * (self.fee_pct / 100), 2)
        print(f"[{self.label}] Fee ({self.fee_pct}%): Rs. {fee:.2f}")
        return channel.process(amt)


class StripeGateway(GatewayBase):
    def __init__(self):
        super().__init__("Stripe", 2.9)

    def dispatch(self, mode: str, amt: float, **creds) -> bool:
        channel = StripeChannelBuilder.make_channel(mode, **creds)
        fee = round(amt * (self.fee_pct / 100), 2)
        print(f"[{self.label}] Fee ({self.fee_pct}%): Rs. {fee:.2f}")
        return channel.process(amt)


class GatewayDirectory:
    providers: dict[str, type[GatewayBase]] = {
        "stripe": StripeGateway,
        "razorpay": RzpGateway,
    }

    @classmethod
    def register_gateway(cls, key: str, gw_cls: type[GatewayBase]) -> None:
        cls.providers[key.lower()] = gw_cls

    @classmethod
    def get_gateway(cls, provider_name: str) -> GatewayBase:
        key = provider_name.strip().lower()
        if key not in cls.providers:
            raise ValueError(f"Unknown gateway: {provider_name}")
        return cls.providers[key]()
