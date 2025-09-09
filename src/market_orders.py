class MarketOrder:
    """Execute market orders immediately at current market price"""
    
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, quantity):
        """Place a market order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
            
        Returns:
            dict: Order response from Binance API
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        # Validate inputs
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        return self.client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="MARKET",
            quantity=quantity
        )