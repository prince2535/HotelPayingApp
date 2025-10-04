import os #import os module for folders and file
import csv
from datetime import datetime #import datetime module to get current date and time

def login_admin():
    USERNAME = "admin" #define admin username
    PASSWORD = "12345"
    
    print("\n--- ADMIN LOGIN ---") #print admin login heading
    username = input("Enter username: ") #ask for username
    password = input("Enter password: ") #ask for password
    
    if username == USERNAME and password == PASSWORD: #check if username and password match
        print("Login successful!") #if match, show success message
        return True 
    else:
        print("Invalid credentials. Access denied.")

def view_all_bills(): #difine a fun. to show all saved bills
    print("\n=====ALL SAVED BILL=====") #print a heading
    
    folder = "bills" #this is a folder which in all bills are save
    
    if not os.path.exists(folder): #check if "bills" folder exist
        print("No bill folder found.") #if folder not found , show message
        return # stope function
    
     # Sort all saved bill files based on the time they were created/saved,
     # so latest bills come first (like how hotel managers want to see today's bills at the top)
    files = sorted(os.listdir(folder), key=lambda x: os.path.getmtime(os.path.join(folder, x))) 
    
    if not files: #if the folder is empty
        print("No bill found.") # show message
        return # stop function
    
    for filename in files: #Loop through each file
        print(f"\n--- {filename}---") #print file name as heading
        with open(os.path.join(folder , filename), "r" , encoding="utf-8") as f: #open the bill file from folder
           print(f.read()) #read and print the full bill content   

def view_today_summary(): #define a function to view today's summary 
     today = datetime.now().strftime("%Y-%m-%d") #get today's date in YYYY-MM-DD format
     total_customers =0
     total_revenue = 0.0     
     
     try:
        #Open the master CSV file that contains all bills
        with open("all_bills_master.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # Read the file as dictionary (column name based)

            for row in reader:  # Loop through each row (each bill)
                bill_date = row["Date/Time"].split(" ")[0]  # Extract only the date part from 'Date/Time'

                if bill_date == today:  # If the bill is from today
                    total_customers += 1  # Count the customer
                    total_revenue += float(row["GrandTotal"])  # Add this bill's grand total to today's revenue
        # after reading all row- show result  
        
            
           
            # show full summary report
            print("\n📊 DAILY REVENUE SUMMARY")
            print(f"📅 Date         : {today}")
            print(f"👥 Customers    : {total_customers}") 
           
        if total_customers == 0:
            print("❌ No bills found for today.")                                      #If no bill from today
        else:    
            print(f"💰 Total Revenue: ₹{total_revenue:.2f}")                           # Total Revenue (.2f - .after two digit print)
            print(f"📈 Avg per Bill : ₹{round( total_revenue / total_customers, 2)}")  # Calculate average revenue per customer
    
     except FileNotFoundError:                                                          # If the master file doesn't exist
        print("\nNo data found. 'all_bills_master.csv' file is missing.")
        
     
         