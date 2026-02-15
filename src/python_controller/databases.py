import sqlite3
import redis
import json
from data_layer import build_candles

r = redis.Redis(host='localhost', port=6379, db=0)

def init_sqlite():
    conn = sqlite3.connect('databases/historical.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY, symbol TEXT, signal TEXT, price REAL, time TEXT, profit REAL)''')
    conn.commit()
    conn.close()

def save_trade_sqlite(symbol, signal, price, time, profit):
    conn = sqlite3.connect('databases/historical.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO trades (symbol, signal, price, time, profit) VALUES (?, ?, ?, ?, ?)", (symbol, signal, price, time, profit))
    conn.commit()
    conn.close()
    print("Trade saved to SQLite.")

def save_real_time_data(key, data):
    r.set(key, json.dumps(data))
    print(f"Real-time data saved to Redis: {key}")

def get_real_time_data(key):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

if __name__ == "__main__":
    init_sqlite()
    save_trade_sqlite("AUDCAD", "Buy", 1.05, "2026-02-13 23:00:00", 50.0)
    save_real_time_data("regime", {"regime": "RANGING"})
    print(get_real_time_data("regime"))