from __future__ import annotations
from abc import ABC, abstractmethod


class PayOption(ABC):
    @abstractmethod
    def summary(self) -> str:
        pass

    @abstractmethod
    def process(self, amt: float) -> bool:
        pass


class RzpCardOption(PayOption):
    def __init__(self, card_no: str):
        self.card_no = card_no.strip()

    def summary(self) -> str:
        tail = self.card_no[-4:] if len(self.card_no) >= 4 else self.card_no
        return f"Razorpay Card (*{tail})"

    def process(self, amt: float) -> bool:
        print(f"Charging Rs. {amt:.2f} through {self.summary()}")
        return True


class RzpUpiOption(PayOption):
    def __init__(self, upi_handle: str):
        self.upi_handle = upi_handle.strip()

    def summary(self) -> str:
        return f"Razorpay UPI ({self.upi_handle})"

    def process(self, amt: float) -> bool:
        print(f"Charging Rs. {amt:.2f} through {self.summary()}")
        return True


class StripeCardOption(PayOption):
    def __init__(self, card_no: str):
        self.card_no = card_no.strip()

    def summary(self) -> str:
        tail = self.card_no[-4:] if len(self.card_no) >= 4 else self.card_no
        return f"Stripe Card (*{tail})"

    def process(self, amt: float) -> bool:
        print(f"Charging Rs. {amt:.2f} through {self.summary()}")
        return True


class StripeUpiOption(PayOption):
    def __init__(self, upi_handle: str):
        self.upi_handle = upi_handle.strip()

    def summary(self) -> str:
        return f"Stripe UPI ({self.upi_handle})"

    def process(self, amt: float) -> bool:
        print(f"Charging Rs. {amt:.2f} through {self.summary()}")
        return True


class ChannelBuilder(ABC):
    builders: dict[str, type[PayOption]] = {}

    @classmethod
    def register(cls, mode: str, option_cls: type[PayOption]) -> None:
        if "builders" not in cls.__dict__:
            cls.builders = dict(cls.builders)
        cls.builders[mode.strip().lower()] = option_cls

    @classmethod
    def make_channel(cls, mode: str, **creds) -> PayOption:
        key = mode.strip().lower()
        if key not in cls.builders:
            raise ValueError(f"Unsupported payment mode: {mode}")
        return cls.builders[key](**creds)


class RzpChannelBuilder(ChannelBuilder):
    builders = {
        "card": RzpCardOption,
        "upi": RzpUpiOption,
    }


class StripeChannelBuilder(ChannelBuilder):
    builders = {
        "card": StripeCardOption,
        "upi": StripeUpiOption,
    }


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


def run_cli() -> None:
    try:
        provider = input("Gateway (stripe / razorpay): ").strip().lower()
        mode = input("Method (card / upi): ").strip().lower()

        if mode == "card":
            card_no = input("Card number: ").strip()
            if not card_no:
                raise ValueError("Card number cannot be blank")
            creds = {"card_no": card_no}
        elif mode == "upi":
            upi_handle = input("UPI ID: ").strip()
            if not upi_handle:
                raise ValueError("UPI ID cannot be blank")
            creds = {"upi_handle": upi_handle}
        else:
            raise ValueError(f"Unsupported payment mode: {mode}")

        amt = float(input("Amount (Rs.): "))
        if amt <= 0:
            raise ValueError("Amount must be greater than zero")

        gw = GatewayDirectory.get_gateway(provider)
        ok = gw.dispatch(mode, amt, **creds)
        if ok:
            print("Transaction done.")
    except ValueError as err:
        print(f"Payment failed: {err}")


if __name__ == "__main__":
    run_cli()
