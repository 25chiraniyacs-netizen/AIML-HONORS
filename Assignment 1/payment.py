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
