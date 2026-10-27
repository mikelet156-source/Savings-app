from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('savings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY, type TEXT, amount INTEGER, phone TEXT, status TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_balance():
    conn = sqlite3.connect('savings.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END),0) FROM transactions WHERE status='success'")
    bal = c.fetchone()[0]
    conn.close()
    return bal

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/balance')
def balance():
    conn = sqlite3.connect('savings.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END),0) FROM transactions WHERE status='success'")
    bal = c.fetchone()[0]
    c.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    transactions = [{"id":r[0],"type":r[1],"amount":r[2],"phone":r[3],"status":r[4],"created_at":r[5]} for r in rows]
    conn.close()
    return jsonify({"balance":bal,"transactions":transactions})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    phone = data.get('phone','')
    amount = int(data.get('amount',0))
    date_now = datetime.now().isoformat()
    
    conn = sqlite3.connect('savings.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, phone, status, date) VALUES (?,?,?,?,?)",
              ('deposit', amount, phone, 'success', date_now))
    conn.commit()
    conn.close()
    
    return jsonify({"success":True,"message":f"UGX {amount} added!","balance":get_balance()})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    phone = data.get('phone','')
    amount = int(data.get('amount',0))
    date_now = datetime.now().isoformat()
    
    if amount > get_balance():
        return jsonify({"success":False,"message":"Insufficient balance"}), 400
    
    conn = sqlite3.connect('savings.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, phone, status, date) VALUES (?,?,?,?,?)",
              ('withdraw', amount, phone, 'success', date_now))
    conn.commit()
    conn.close()
    
    return jsonify({"success":True,"message":f"UGX {amount} withdrawn!","balance":get_balance()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
