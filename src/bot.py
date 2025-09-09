import logging
from market_orders import MarketOrder
from limit_orders import LimitOrder
from advanced.stop_limit import StopLimitOrder
from advanced.oco import OCOOrder
from advanced.twap import TWAPOrder


# Basic Bot Implementation for Binance Futures Testnet using various order types 
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):   # testnet=True for Futures Testnet 
        # Initialize Binance Client 
        from binance import Client
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.setup_logger()
        self.logger.info("Bot initialized on Binance Futures Testnet.")

    def setup_logger(self):                                  # Simple file logger setup 
        self.logger = logging.getLogger("BasicBot")
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler("bot.log")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def place_market_order(self, symbol, side, quantity):
        try:
            order = MarketOrder(self.client).place_order(symbol, side, quantity)
            self.logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Market order failed: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = LimitOrder(self.client).place_order(symbol, side, quantity, price)
            self.logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Limit order failed: {e}")
            return None


# Advanced Orders for Binance Futures Testnet 
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = StopLimitOrder(self.client).place_order(symbol, side, quantity, stop_price, limit_price)
            self.logger.info(f"Stop-Limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Stop-Limit order failed: {e}")
            return None

    def place_oco_order(self, symbol, side, quantity, take_profit_price, stop_price):
        try:
            order = OCOOrder(self.client, self.logger).place_order(
                symbol, side, quantity, take_profit_price, stop_price
            )
            return order
        except Exception as e:
            self.logger.error(f"OCO order failed: {e}")
            return None

    def place_twap_order(self, symbol, side, total_quantity, chunks=5, interval=10):
        try:
            orders = TWAPOrder(self.client, self.logger).place_order(
                symbol, side, total_quantity, chunks, interval
            )
            return orders
        except Exception as e:
            self.logger.error(f"TWAP order failed: {e}")
            return None


# Example usage and testing of the BasicBot class 
if __name__ == "__main__":
    print("=== Binance Futures Testnet Bot ===")
    api_key = input("Enter your API Key: ").strip()
    api_secret = input("Enter your Secret Key: ").strip()

    # Initialize the bot and check api keys 
    bot = BasicBot(api_key, api_secret)

    print("\nSelect Order Type:")
    print("1. Market Order\n2. Limit Order\n3. Stop-Limit Order\n4. OCO Order\n5. TWAP Order")
    choice = input("Choice (1-5): ").strip()

    symbol = input("Symbol (e.g., BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    quantity = float(input("Quantity: "))

    if choice == "1":
        bot.place_market_order(symbol, side, quantity)
    elif choice == "2":
        price = float(input("Price: "))
        bot.place_limit_order(symbol, side, quantity, price)
    elif choice == "3":
        stop_price = float(input("Stop Price: "))
        limit_price = float(input("Limit Price: "))
        bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    elif choice == "4":
        take_profit_price = float(input("Take Profit Price: "))
        stop_price = float(input("Stop Price: "))
        bot.place_oco_order(symbol, side, quantity, take_profit_price, stop_price)
    elif choice == "5":
        chunks = int(input("Number of chunks: "))
        interval = int(input("Interval between chunks (seconds): "))
        bot.place_twap_order(symbol, side, quantity, chunks, interval)
    else:
        print("Invalid choice!")
