class LimitOrder:
    """Place limit orders at specific price levels"""
    
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, quantity, price):
        """Place a limit order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
            price (float): Desired price level
            
        Returns:
            dict: Order response from Binance API
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        # Validate inputs
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if price <= 0:
            raise ValueError("Price must be positive")
        
        return self.client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )