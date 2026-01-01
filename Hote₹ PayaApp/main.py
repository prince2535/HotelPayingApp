# ===============================
# main.py — Hotel Billing System
# ===============================

# 📦 Step 1: Import all needed modules and functions from other files
from exporter import export_to_csv   # Function to export bill data to a CSV file
from menu import menu                # Menu dictionary containing item names and prices
from customer import Customer        # Customer class to store customer info
from billing import Order             # Order class to store item orders
from admin import login_admin, view_all_bills, view_today_summary  # Admin login and report functions
from datetime import datetime        # For current date and time
import os                            # For folder and file handling
import csv                           # For working with CSV files

# ===============================
# Step 2: Get customer details
# ===============================
def get_customer_info():
    """Ask for customer name, mobile number, and optional room number"""
    name = input("Enter customer name: ").strip()  # Remove extra spaces
    mobile = input("Enter mobile number: ").strip()
    room_no = input("Enter room number (press Enter if not staying): ").strip()
    return Customer(name, mobile), room_no         # Return a Customer object and room number

# ===============================
# Step 3: Print bill to console
# ===============================
def print_bill(customer, orders, subtotal, service_charge, gst, grand_total,
               discount_amount, discount_percentage, room_no, bill_time):
    """Display the bill in a nice format on the screen"""
    print("\n" + "="*40)
    print(" " * 13 + " HOTEL BILL ")
    print("-" * 40)
    print(f"Customer: {customer.name}")
    print(f"Mobile: {customer.mobile}")
    if room_no:  # Only print room number if customer is staying
        print(f"Room Number: {room_no}")
    print(f"Date/Time: {bill_time}")
    print("-" * 40)
    
    print(f"{'Item':15}{'Qty':>5} {'Price':>7} {'Total':>7}")
    print("-" * 40)
    for order in orders:
        # Print each item with quantity, price, and total
        print(f"{order.item_name:15}{order.quantity:>5} ₹{order.price_per_item:>7} ₹{order.total_price():>7}")
    print("-" * 40)
    print(f"Subtotal: ₹{subtotal}")
    print(f"Discount ({discount_percentage}%): -₹{discount_amount}")
    print(f"Service Charge (10%): ₹{service_charge}")
    print(f"GST (18%): ₹{gst}")
    print(f"Total Amount: ₹{grand_total}")
    print("=" * 40)
    print("Thank you! Visit again.")

# ===============================
# Step 4: Save bill data to master CSV
# ===============================
def save_master_summary(customer, room_no, subtotal, service_charge, gst, grand_total,
                        bill_time, discount_amount, discount_percentage, orders):
    """Save bill details to master CSV file and print the bill"""
    with open("all_bills_master.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([bill_time, customer.name, customer.mobile, room_no,
                         subtotal, service_charge, gst, grand_total])
    # Print bill after saving data
    print_bill(customer, orders, subtotal, service_charge, gst, grand_total,
               discount_amount, discount_percentage, room_no, bill_time)

# ===============================
# Step 5: Create a new bill
# ===============================
def create_new_bill():
    """Handles the full process of making a new bill"""
    orders = []  # Empty list to store all ordered items
    customer, room_no = get_customer_info()  # Get customer info

    # 📝 Take orders from the customer
    while True:
        print("\n---- MENU ----")
        for item, price in menu.items():  # Show menu items
            print(f"{item}: ₹{price}")
        
        item_name = input("\nEnter item name (or 'done' to finish): ").strip().lower()
        if item_name == "done":
            break  # Exit the order loop
        if item_name not in menu:
            print("❌ Item not available!")
            continue
        
        try:
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("❌ Invalid quantity! Try again.")
            continue
        
        # Store the order
        orders.append(Order(item_name, qty, menu[item_name]))

    if not orders:
        print("⚠️ No items ordered. Bill not generated.")
        return

    # 🎯 Get discount (if any)
    try:
        discount_percentage = float(input("Enter discount % (or 0 if none): "))
    except ValueError:
        discount_percentage = 0

    # 💰 Calculate totals
    subtotal = sum(order.total_price() for order in orders)
    discount_amount = round((discount_percentage / 100) * subtotal, 2)
    discount_total = subtotal - discount_amount
    service_charge = round(0.10 * discount_total, 2)
    gst = round(0.18 * discount_total, 2)
    grand_total = round(discount_total + service_charge + gst, 2)

    # 📅 Date and Time
    now = datetime.now()
    bill_time = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # 📂 Create folder for bills
    os.makedirs("bills", exist_ok=True)
    filename = f"bills/{customer.name}_{timestamp}_bill.txt"

    # 📝 Save bill to text file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 30 + "\n")
        f.write(" " * 10 + "HOTEL BILL\n")
        f.write("=" * 30 + "\n")
        f.write(f"Customer Name : {customer.name}\n")
        f.write(f"Mobile Number : {customer.mobile}\n")
        if room_no:
            f.write(f"Room Number   : {room_no}\n")
        f.write(f"Date/Time     : {bill_time}\n")
        f.write("-" * 30 + "\n")
        f.write(f"{'Item':<12}{'Qty':<6}{'Amount'}\n")
        f.write("-" * 30 + "\n")
        for order in orders:
            f.write(f"{order.item_name:<12}{order.quantity:<6}₹{order.total_price()}\n")
        f.write("-" * 30 + "\n")
        f.write(f"{'Subtotal':<18}₹{subtotal}\n")
        f.write(f"{f'Discount ({discount_percentage}%)':<18}-₹{discount_amount}\n")
        f.write(f"{'Service Charge (10%)':<18}₹{service_charge}\n")
        f.write(f"{'GST (18%)':<18}₹{gst}\n")
        f.write("-" * 30 + "\n")
        f.write(f"{'Total Amount':<18}₹{grand_total}\n")
        f.write("=" * 30 + "\n")
        f.write("Thank you! Visit again.\n")
        f.write("=" * 30 + "\n")

    # 💾 Save to master CSV and export individual CSV
    save_master_summary(customer, room_no, subtotal, service_charge, gst,
                        grand_total, bill_time, discount_amount, discount_percentage, orders)
    export_to_csv(customer.name, customer.mobile, room_no, subtotal, service_charge, gst, grand_total, bill_time)

# ===============================
# Step 6: Main Program Menu
# ===============================
while True:
    print("\n--- MAIN MENU ---")
    print("1. Create New Bill")
    print("2. Admin Dashboard")
    print("3. Exit")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        create_new_bill()  # Start billing process
    elif choice == "2":
        if login_admin():  # Ask admin login
            print("\n--- ADMIN DASHBOARD ---")
            print("1. View All Bills")
            print("2. View Today's Summary")
            admin_choice = input("Enter choice: ").strip()
            if admin_choice == "1":
                view_all_bills()  # Show all saved bills
            elif admin_choice == "2":
                view_today_summary()  # Show today’s report
            else:
                print("❌ Invalid choice.")
        else:
            print("❌ Login failed.")
    elif choice == "3":
        print("👋 Exiting. Goodbye!")
        break  # Exit program
    else:
        print("❌ Invalid choice. Please try again.")
