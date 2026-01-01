# ==============================
# app.py — Flask Server (Step-18 with PDF + HTML UI)
# ==============================

from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, session
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont




app = Flask(__name__)
app.Secret_key = 'your_secret_key'

# Admin Login Page
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid credentials", 401

    return render_template("admin_login.html")

# Example admin credentials (for demo)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"



# -------------------------
# Menu Data
# -------------------------
menu = {
    "Tea": 10,
    "Coffee": 20,
    "Sandwich": 50,
    "Burger": 60,
    "Pizza": 120,
    "Room Stay (1 night)": 1000
}

# Ensure bills folder exists
if not os.path.exists("bills"):
    os.makedirs("bills")

# -------------------------
# Routes
# -------------------------




@app.route("/")
def home():
    return "Welcome to Hotel Billing API!"

# Show billing UI (HTML page)
@app.route("/billing")
def billing_page():
    return render_template("index.html")

# Return menu as JSON
@app.route("/menu")
def get_menu():
    return jsonify(menu)

# Place order & return bill (JSON + save PDF)
@app.route("/order", methods=["POST"])
def place_order():
    data = request.json
    customer_name = data.get("customer_name")
    items = data.get("items", [])

    orders = []
    total = 0

    # Calculate totals
    for it in items:
        name = it["name"]
        qty = it["qty"]

        if name not in menu:
            return jsonify({"error": f"Item '{name}' not available"}), 400

        price = menu[name]
        item_total = price * qty
        orders.append({"item": name, "qty": qty, "price": price, "total": item_total})
        total += item_total

    # Charges
    service_charge = round(0.10 * total, 2)
    gst = round(0.18 * total, 2)
    grand_total = round(total + service_charge + gst, 2)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Final Bill JSON
    bill = {
        "customer_name": customer_name,
        "datetime": now,
        "orders": orders,
        "subtotal": total,
        "service_charge": service_charge,
        "gst": gst,
        "grand_total": grand_total
    }

    # Save bill as PDF
    filename = f"bills/{customer_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf_bill(filename, bill)

    bill["pdf_file"] = filename.split("/")[-1]  # return filename only
    return jsonify(bill)

# Download saved bill
@app.route("/download/<filename>")
def download_bill(filename):
    return send_file(f"bills/{filename}", as_attachment=True)

# -------------------------
# PDF Generation Function
# -------------------------
def generate_pdf_bill(filename, bill):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "HOTEL BILL")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Customer: {bill['customer_name']}")
    c.drawString(50, 750, f"Date/Time: {bill['datetime']}")

    # Table header
    c.drawString(50, 720, "Item")
    c.drawString(250, 720, "Qty")
    c.drawString(300, 720, "Price")
    c.drawString(400, 720, "Total")

    y = 700
    for o in bill["orders"]:
        c.drawString(50, y, o["item"])
        c.drawString(250, y, str(o["qty"]))
        c.drawString(300, y, f"₹{o['price']}")
        c.drawString(400, y, f"₹{o['total']}")
        y -= 20

    # Totals
    y -= 20
    c.drawString(50, y, f"Subtotal: ₹{bill['subtotal']}")
    y -= 20
    c.drawString(50, y, f"Service Charge (10%): ₹{bill['service_charge']}")
    y -= 20
    c.drawString(50, y, f"GST (18%): ₹{bill['gst']}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Grand Total: ₹{bill['grand_total']}")

    c.save()

if __name__ == "__main__":
    app.run(debug=True)
