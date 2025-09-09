import time

class TWAPOrder:
    """
    Split a large order into smaller chunks over a time interval.
    Example: buy 10 BTC in 5 chunks every 10 seconds.
    """
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, total_quantity, chunks=5, interval=10):
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        qty_per_chunk = round(total_quantity / chunks, 8)
        executed_orders = []

        try:
            for i in range(chunks):
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=qty_per_chunk
                )
                executed_orders.append(order)
                if self.logger:
                    self.logger.info(f"TWAP chunk {i+1}/{chunks} executed: {order}")
                time.sleep(interval)
            return executed_orders
        except Exception as e:
            if self.logger:
                self.logger.error(f"TWAP order failed: {e}")
            raise
