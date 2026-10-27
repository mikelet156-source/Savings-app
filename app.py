from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os, requests, uuid
from datetime import datetime
app=Flask(__name__)
CORS(app)
DB='savings.db'
def init_db():
 conn=sqlite3.connect(DB)
 c=conn.cursor()
 c.execute('CREATE TABLE IF NOT EXISTS transactions (id TEXT PRIMARY KEY, type TEXT, amount INTEGER, phone TEXT, status TEXT, created_at TEXT)')
 conn.commit()
 conn.close()
init_db()
def get_balance():
 conn=sqlite3.connect(DB)
 c=conn.cursor()
 c.execute("SELECT COALESCE(SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END),0) FROM transactions WHERE status='success'")
 bal=c.fetchone()[0]
 conn.close()
 return bal
@app.route('/')
def home():
 return jsonify({"status":"API running"})
@app.route('/balance')
def balance():
 conn=sqlite3.connect(DB)
 c=conn.cursor()
 c.execute("SELECT COALESCE(SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END),0) FROM transactions WHERE status='success'")
 bal=c.fetchone()[0]
 c.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 20")
 txs=[{"id":r[0],"type":r[1],"amount":r[2],"phone":r[3],"status":r[4],"created_at":r[5]} for r in c.fetchall()]
 conn.close()
 return jsonify({"balance":bal,"transactions":txs})
@app.route('/deposit',methods=['POST'])
def deposit():
 data=request.json
 phone=data.get('phone','')
 amount=int(data.get('amount',0))
 tx_id=str(uuid.uuid4())[:8]
 conn=sqlite3.connect(DB)
 c=conn.cursor()
 c.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",(tx_id,"deposit",amount,phone,"success",datetime.now().isoformat()))
 conn.commit()
 conn.close()
 return jsonify({"success":True,"message":f"UGX {amount} added"})
@app.route('/withdraw',methods=['POST'])
def withdraw():
 data=request.json
 phone=data.get('phone','')
 amount=int(data.get('amount',0))
 tx_id=str(uuid.uuid4())[:8]
 conn=sqlite3.connect(DB)
 c=conn.cursor()
 c.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",(tx_id,"withdraw",amount,phone,"success",datetime.now().isoformat()))
 conn.commit()
 conn.close()
 return jsonify({"success":True,"message":f"UGX {amount} sent"})
if __name__=='__main__':
 port=int(os.environ.get("PORT",5000))
 app.run(host='0.0.0.0',port=port)
