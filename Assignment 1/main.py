from aggregator import GatewayDirectory


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
