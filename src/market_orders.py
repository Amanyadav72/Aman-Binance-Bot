class MarketOrder:
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, quantity):
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        return self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
