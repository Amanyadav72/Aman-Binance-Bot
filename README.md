

---

# Binance Futures Testnet Trading Bot

**A Python-based trading bot for Binance USDT-M Futures Testnet supporting Market, Limit, Stop-Limit, OCO, and TWAP orders with robust logging, error handling and CLI interface.**

---

## **Table of Contents**

* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Order Types](#order-types)
* [Logging](#logging)
* [Contributing](#contributing)
* [License](#license)

---

## **Features**

* Place **Market Orders** and **Limit Orders**
* Execute **Stop-Limit Orders** (triggered when stop price is hit)
* Simulate **OCO Orders** (Take-Profit + Stop-Loss simultaneously)
* Implement **TWAP Orders** (split large orders into smaller chunks over time)
* **CLI Interface**: easy input of API keys, symbol, side, quantity, and prices
* **Robust logging** of API calls, executions, and errors
* Modular and reusable **Python package structure** for future extensions

---

## **Project Structure**

```
[project_root]/
│
├── src/                    # Source code
│   ├── __init__.py
│   ├── bot.py              # Main bot with CLI
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── advanced/
│   │   ├── __init__.py
│   │   ├── stop_limit.py
│   │   ├── oco.py
│   │   └── twap.py
│
├── bot.log                 # Log file (generated during execution)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## **Installation**

1. **Clone the repository**

```bash
git clone <repository_url>
cd <project_root>
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

* Windows: `venv\Scripts\activate`
* Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## **Usage**

1. Run the bot

```bash
cd src
python bot.py
```
## 🖥️📸 Screenshots
![CLI view] 
<img width="687" height="466" alt="Screenshot 2025-09-10 122652" src="https://github.com/user-attachments/assets/07693c81-1499-497d-9207-d9e8d2b21070" />

2. Enter **API Key** and **Secret Key** (Binance Testnet- Get testnet keys: https://testnet.binancefuture.com ) when prompted.

3. Follow CLI prompts:

   * Select **order type** (Market, Limit, Stop-Limit, OCO, TWAP)
   * Enter **symbol** (e.g., `BTCUSDT`)
   * Enter **side** (`BUY` or `SELL`)
   * Enter **quantity** and **price parameters** (if applicable)

4. Execution results and logs are saved in `bot.log`.

---

## **Order Types**

| Order Type      | Description                                                              |
| --------------- | ------------------------------------------------------------------------ |
| Market          | Immediate execution at the current market price                          |
| Limit           | Buy/Sell at a specified price                                            |
| Stop-Limit      | Place a limit order when the stop price is triggered                     |
| OCO (Simulated) | Place Take-Profit + Stop-Loss simultaneously to automate exit strategies |
| TWAP            | Split large orders into smaller chunks over time for gradual execution   |

---

## **Logging**

* All API requests, order executions, and errors are logged in `bot.log`
* Example log entries:

```
2025-09-09 21:00:01 - INFO - Market order placed: {'orderId': 123456, 'symbol': 'BTCUSDT', ...}
2025-09-09 21:05:12 - ERROR - Limit order failed: insufficient balance
```

---

## **Contributing**

* Fork the repository and create a branch for your feature/fix.
* Submit a pull request with a detailed description.
* Suggestions and improvements for additional order types, UI, or strategies are welcome.

---

## **License**

This project is released under the MIT License. See `LICENSE` file for details.

---

### Optional Enhancement Notes (Future)

* Add **Graphical UI** using Tkinter or Flask for a more interactive experience.
* Implement **Grid Trading** strategy for automated buy-low/sell-high.
* Add **WebSocket support** for real-time price tracking and smarter execution.

---


