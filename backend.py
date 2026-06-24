from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          # change if needed
    password="root",      # your MySQL password
    database="foodorderdb"
)

@app.route("/")
def home():
    return render_template("frontend.html")

# 🟢 Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify({"status": "success", "message": "✅ Login Successful!"})
    else:
        return jsonify({"status": "fail", "message": "❌ Invalid Credentials!"})

# 🟢 Create Order
@app.route("/order", methods=["POST"])
def order():
    item = request.form["item"]
    qty = int(request.form["quantity"])
    cursor = db.cursor()

    cursor.execute("SELECT price FROM menu WHERE name=%s", (item,))
    price = cursor.fetchone()[0]
    total = price * qty

    cursor.execute("INSERT INTO orders (item, quantity, total) VALUES (%s, %s, %s)", (item, qty, total))
    db.commit()
    cursor.close()
    return "✅ Ordered Successfully!"

# 🔵 Read Orders
@app.route("/orders", methods=["GET"])
def get_orders():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    return jsonify(orders)

# 🟡 Update Order
@app.route("/update/<int:order_id>", methods=["POST"])
def update_order(order_id):
    qty = int(request.form["quantity"])
    cursor = db.cursor()

    cursor.execute("SELECT item FROM orders WHERE id=%s", (order_id,))
    item = cursor.fetchone()[0]

    cursor.execute("SELECT price FROM menu WHERE name=%s", (item,))
    price = cursor.fetchone()[0]
    total = price * qty

    cursor.execute("UPDATE orders SET quantity=%s, total=%s WHERE id=%s", (qty, total, order_id))
    db.commit()
    cursor.close()
    return "🔄 Order Updated Successfully!"

# 🔴 Delete Order
@app.route("/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))
    db.commit()
    cursor.close()
    return "❌ Order Deleted Successfully!"

if __name__ == "__main__":
    app.run(debug=True)
 