class OCOOrder:
    """Simulate OCO (One-Cancels-Other) orders for Futures"""
    
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, quantity, take_profit_price, stop_price):
        """Place OCO order (Take-Profit + Stop-Loss)
        
        Args:
            symbol (str): Trading pair
            side (str): Original position side ('BUY' or 'SELL')
            quantity (float): Position size to close
            take_profit_price (float): Take profit level
            stop_price (float): Stop loss level
            
        Returns:
            list: List of both orders [take_profit_order, stop_loss_order]
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        # Validate inputs
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if take_profit_price <= 0 or stop_price <= 0:
            raise ValueError("Prices must be positive")
        
        # Validate price logic
        if side == "BUY":
            if take_profit_price <= stop_price:
                raise ValueError("For BUY positions: take_profit_price must be > stop_price")
        else:  # SELL
            if take_profit_price >= stop_price:
                raise ValueError("For SELL positions: take_profit_price must be < stop_price")

        orders = []
        try:
            # Determine closing side (opposite of original position)
            close_side = "SELL" if side == "BUY" else "BUY"
            
            # Fixed: Use reduceOnly instead of closePosition for better control
            # Take-profit order
            tp_order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=close_side,
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit_price,
                quantity=quantity,
                reduceOnly=True
            )
            orders.append(tp_order)
            
            # Stop-loss order
            sl_order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=close_side,
                type="STOP_MARKET",
                stopPrice=stop_price,
                quantity=quantity,
                reduceOnly=True
            )
            orders.append(sl_order)

            if self.logger:
                self.logger.info(f"OCO orders placed: TP={tp_order['orderId']}, SL={sl_order['orderId']}")
            
            return orders
            
        except Exception as e:
            # Rollback: Cancel any successfully placed orders
            for order in orders:
                try:
                    self.client.futures_cancel_order(
                        symbol=symbol.upper(), 
                        orderId=order['orderId']
                    )
                    if self.logger:
                        self.logger.info(f"Cancelled order {order['orderId']} due to OCO failure")
                except:
                    pass
            
            if self.logger:
                self.logger.error(f"OCO order failed: {e}")
            raise