class StopLimitOrder:
    """Place stop-limit orders (conditional orders)"""
    
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place a stop-limit order
        
        Args:
            symbol (str): Trading pair
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
            stop_price (float): Trigger price
            limit_price (float): Limit price after trigger
            
        Returns:
            dict: Order response from Binance API
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        # Validate inputs
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if stop_price <= 0 or limit_price <= 0:
            raise ValueError("Prices must be positive")
        
        # Fixed: Use STOP type instead of STOP_MARKET for stop-limit
        return self.client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price
        )