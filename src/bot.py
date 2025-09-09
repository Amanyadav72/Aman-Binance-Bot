import logging
import sys
import os
from market_orders import MarketOrder
from limit_orders import LimitOrder
from advanced.stop_limit import StopLimitOrder
from advanced.oco import OCOOrder
from advanced.twap import TWAPOrder


class SimplifiedBot:
    """Simplified CLI-based trading bot for Binance Futures Testnet"""
    
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize the trading bot
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Use testnet (True) or live trading (False)
        """
        self.testnet = testnet
        self.setup_logger()
        
        # Validate API credentials
        if not api_key or not api_secret:
            raise ValueError("❌ API key and secret are required")
        
        try:
            from binance import Client
            self.client = Client(api_key, api_secret, testnet=testnet)
            
            # Test connection
            self.client.futures_account()
            
            env = "Testnet" if testnet else "Live"
            self.logger.info(f"✅ Bot initialized on Binance Futures {env}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize bot: {str(e)}")
            raise

    def setup_logger(self):
        """Setup logging to file and console"""
        self.logger = logging.getLogger("SimplifiedBot")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # File handler
        fh = logging.FileHandler("bot.log")
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def place_market_order(self, symbol, side, quantity):
        """Place market order"""
        try:
            order = MarketOrder(self.client).place_order(symbol, side, quantity)
            self.logger.info(f"✅ Market order executed: {order['orderId']}")
            return order
        except Exception as e:
            self.logger.error(f"❌ Market order failed: {str(e)}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Place limit order"""
        try:
            order = LimitOrder(self.client).place_order(symbol, side, quantity, price)
            self.logger.info(f"✅ Limit order placed: {order['orderId']}")
            return order
        except Exception as e:
            self.logger.error(f"❌ Limit order failed: {str(e)}")
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place stop-limit order"""
        try:
            order = StopLimitOrder(self.client).place_order(symbol, side, quantity, stop_price, limit_price)
            self.logger.info(f"✅ Stop-limit order placed: {order['orderId']}")
            return order
        except Exception as e:
            self.logger.error(f"❌ Stop-limit order failed: {str(e)}")
            return None

    def place_oco_order(self, symbol, side, quantity, take_profit_price, stop_price):
        """Place OCO order"""
        try:
            orders = OCOOrder(self.client, self.logger).place_order(
                symbol, side, quantity, take_profit_price, stop_price
            )
            self.logger.info(f"✅ OCO orders placed: {len(orders)} orders")
            return orders
        except Exception as e:
            self.logger.error(f"❌ OCO order failed: {str(e)}")
            return None

    def place_twap_order(self, symbol, side, total_quantity, chunks=5, interval=10):
        """Place TWAP order"""
        try:
            orders = TWAPOrder(self.client, self.logger).place_order(
                symbol, side, total_quantity, chunks, interval
            )
            self.logger.info(f"✅ TWAP completed: {len(orders)} chunks executed")
            return orders
        except Exception as e:
            self.logger.error(f"❌ TWAP order failed: {str(e)}")
            return None

    def get_account_info(self):
        """Get account balance and positions"""
        try:
            account = self.client.futures_account()
            balance = float(account['totalWalletBalance'])
            self.logger.info(f"💰 Account Balance: {balance} USDT")
            return account
        except Exception as e:
            self.logger.error(f"❌ Failed to get account info: {str(e)}")
            return None


def get_user_input(prompt, input_type=str, validator=None):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("❌ Input cannot be empty. Please try again.")
                continue
            
            # Convert to desired type
            if input_type == float:
                value = float(user_input)
            elif input_type == int:
                value = int(user_input)
            else:
                value = user_input
            
            # Apply validator if provided
            if validator and not validator(value):
                print("❌ Invalid input. Please try again.")
                continue
            
            return value
            
        except ValueError:
            print(f"❌ Invalid {input_type.__name__} format. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user.")
            return None


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("🚀 SIMPLIFIED BINANCE FUTURES TRADING BOT")
    print("="*60)
    print("📋 Available Order Types:")
    print("  1. 🎯 Market Order    - Execute immediately at market price")
    print("  2. 📌 Limit Order     - Set your desired price")
    print("  3. 🛑 Stop-Limit      - Conditional order with trigger")
    print("  4. 🎭 OCO Order       - Take-Profit + Stop-Loss combo")
    print("  5. ⏱️  TWAP Order      - Split order over time")
    print("  6. 💰 Account Info    - Check balance and positions")
    print("  0. 🚪 Exit")
    print("="*60)


def main():
    """Main CLI interface"""
    print("🔥 Welcome to Simplified Futures Trading Bot")
    print("⚠️  TESTNET MODE - Safe for learning and testing")
    print("💡 Get testnet keys: https://testnet.binancefuture.com\n")
    
    # Get API credentials
    api_key = get_user_input("🔑 Enter your Testnet API Key: ")
    if not api_key:
        return
    
    api_secret = get_user_input("🔐 Enter your Testnet Secret Key: ")
    if not api_secret:
        return
    
    # Initialize bot
    try:
        print("\n⏳ Connecting to Binance Futures Testnet...")
        bot = SimplifiedBot(api_key, api_secret, testnet=True)
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return
    
    # Main trading loop
    while True:
        try:
            display_menu()
            choice = get_user_input("👆 Select option (0-6): ")
            
            if choice == "0":
                print("👋 Goodbye! Happy trading!")
                break
            elif choice == "6":
                bot.get_account_info()
                continue
            elif choice not in ["1", "2", "3", "4", "5"]:
                print("❌ Invalid choice! Please select 0-6.")
                continue
            
            # Get common parameters
            print(f"\n📊 Setting up your order...")
            symbol = get_user_input("📊 Symbol (e.g., BTCUSDT): ").upper()
            side = get_user_input("📈 Side (BUY/SELL): ", validator=lambda x: x.upper() in ["BUY", "SELL"]).upper()
            
            print(f"\n⏳ Processing {['Market', 'Limit', 'Stop-Limit', 'OCO', 'TWAP'][int(choice)-1]} order...")
            
            # Execute based on choice
            if choice == "1":  # Market Order
                quantity = get_user_input("📦 Quantity: ", float, lambda x: x > 0)
                result = bot.place_market_order(symbol, side, quantity)
                
            elif choice == "2":  # Limit Order
                quantity = get_user_input("📦 Quantity: ", float, lambda x: x > 0)
                price = get_user_input("💰 Limit Price: ", float, lambda x: x > 0)
                result = bot.place_limit_order(symbol, side, quantity, price)
                
            elif choice == "3":  # Stop-Limit Order
                quantity = get_user_input("📦 Quantity: ", float, lambda x: x > 0)
                stop_price = get_user_input("🛑 Stop Price: ", float, lambda x: x > 0)
                limit_price = get_user_input("💰 Limit Price: ", float, lambda x: x > 0)
                result = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                
            elif choice == "4":  # OCO Order
                quantity = get_user_input("📦 Quantity: ", float, lambda x: x > 0)
                take_profit_price = get_user_input("🎯 Take Profit Price: ", float, lambda x: x > 0)
                stop_price = get_user_input("🛑 Stop Loss Price: ", float, lambda x: x > 0)
                result = bot.place_oco_order(symbol, side, quantity, take_profit_price, stop_price)
                
            elif choice == "5":  # TWAP Order
                total_quantity = get_user_input("📦 Total Quantity: ", float, lambda x: x > 0)
                chunks = get_user_input("📊 Number of chunks (default 5): ", int, lambda x: x > 0) or 5
                interval = get_user_input("⏱️  Interval seconds (default 10): ", int, lambda x: x > 0) or 10
                result = bot.place_twap_order(symbol, side, total_quantity, chunks, interval)
            
            if result:
                print("✅ Order completed successfully!")
                print("📄 Check 'bot.log' for detailed information.")
            else:
                print("❌ Order failed! Check logs for details.")
            
            input("\n📱 Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            input("📱 Press Enter to continue...")


if __name__ == "__main__":
    main()