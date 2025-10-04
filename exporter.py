# Step 1: Define a function to export bill data to CSV file
def export_to_csv(name, mobile, room_no, subtotal, service_charge, gst, grand_total, bill_time):
    # Step 2: Open or create the file all_bills_master.csv in append mode
    with open("all_bills_master.csv", "a", encoding="utf-8") as f:
        # Step 3: Check if the file is empty (file pointer at start)
        if f.tell() == 0:
            # Step 4: If file is empty, write header (column names)
            f.write("Date/Time,Name,Mobile,Room,Subtotal,ServiceCharge,GST,GrandTotal\n")

        # Step 5: Add the bill data in comma-separated format (CSV row)
        f.write(f"{bill_time},{name},{mobile},{room_no},{subtotal},{service_charge},{gst},{grand_total}\n")
