import time

class TWAPOrder:
    """Time-Weighted Average Price orders - split large orders over time"""
    
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, total_quantity, chunks=5, interval=10):
        """Execute TWAP order strategy
        
        Args:
            symbol (str): Trading pair
            side (str): 'BUY' or 'SELL'
            total_quantity (float): Total amount to trade
            chunks (int): Number of smaller orders
            interval (int): Seconds between each order
            
        Returns:
            list: List of executed orders
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        # Validate inputs
        if total_quantity <= 0:
            raise ValueError("Total quantity must be positive")
        if chunks <= 0:
            raise ValueError("Chunks must be positive")
        if interval <= 0:
            raise ValueError("Interval must be positive")
        
        # Fixed: Better chunk calculation to ensure exact total
        base_chunk_size = total_quantity / chunks
        chunks_list = [base_chunk_size] * (chunks - 1)
        # Last chunk gets the remainder to ensure exact total
        last_chunk = total_quantity - sum(chunks_list)
        chunks_list.append(last_chunk)
        
        executed_orders = []

        try:
            for i, chunk_size in enumerate(chunks_list):
                if chunk_size <= 0:
                    continue
                    
                order = self.client.futures_create_order(
                    symbol=symbol.upper(),
                    side=side,
                    type="MARKET",
                    quantity=round(chunk_size, 8)
                )
                executed_orders.append(order)
                
                if self.logger:
                    self.logger.info(f"TWAP chunk {i+1}/{chunks} executed: {order}")
                
                # Don't sleep after the last chunk
                if i < len(chunks_list) - 1:
                    if self.logger:
                        self.logger.info(f"Waiting {interval} seconds before next chunk...")
                    time.sleep(interval)
            
            if self.logger:
                total_executed = sum(float(order.get('executedQty', 0)) for order in executed_orders)
                self.logger.info(f"TWAP completed: {total_executed}/{total_quantity}")
            
            return executed_orders
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"TWAP order failed: {e}")
            raise