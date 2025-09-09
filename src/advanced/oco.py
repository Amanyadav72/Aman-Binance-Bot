class OCOOrder:
    """
    Place a Take-Profit / Stop-Loss OCO order in Futures.
    NOTE: Binance Futures does not have native OCO, we simulate by placing
    a TAKE_PROFIT_MARKET and STOP_MARKET simultaneously.
    """
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, quantity, take_profit_price, stop_price):
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")

        orders = []
        try:
            # Take-profit
            tp_side = "SELL" if side == "BUY" else "BUY"
            tp_order = self.client.futures_create_order(
                symbol=symbol,
                side=tp_side,
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit_price,
                closePosition=True
            )
            orders.append(tp_order)
            # Stop-loss
            sl_order = self.client.futures_create_order(
                symbol=symbol,
                side=tp_side,
                type="STOP_MARKET",
                stopPrice=stop_price,
                closePosition=True
            )
            orders.append(sl_order)

            if self.logger:
                self.logger.info(f"OCO simulated orders placed: {orders}")
            return orders
        except Exception as e:
            if self.logger:
                self.logger.error(f"OCO order failed: {e}")
            raise
