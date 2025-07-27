# ============================================
# 📌 Personal Budget Tracker
# Author: Shandara Mae De Las Llagas
# Description: A Python console app to track income and expenses. Stores data in CSV and provides summary reports.
# ============================================

# Ensure data folder and file exist
# Read user input for transaction details
# Display total income, expenses, and balance
# List all transactions from CSV file
# Show total spending by category
# Reset all CSV data after confirmation
# Main menu and input handling


import csv
import os
from datetime import datetime

# Constants
DATA_FOLDER = "data"
FILENAME = os.path.join(DATA_FOLDER, "transactions.csv")

# Setup File
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Type", "Amount", "Category", "Note"])

# Functions

def add_transaction():
    print("\n Add New Transaction")
    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print(" Invalid type. Must be 'income' or 'expense'.\n")
        return

    try:
        raw = input("Amount: ")
        clean = raw.replace("₱", "").replace(",", "").strip()
        amount = round(float(clean), 2)
    except ValueError:
        print(" Please enter a valid number.\n")
        return

    category = input("Category (e.g., food, salary): ")
    note = input("Note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, t_type, amount, category, note])

    print("✅ Transaction saved!\n")

def view_summary():
    income = 0
    expenses = 0
    with open(FILENAME, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] == "income":
                income += float(row["Amount"])
            elif row["Type"] == "expense":
                expenses += float(row["Amount"])

    balance = income - expenses
    print("\n📊 Overall Summary")
    print(f"  💰 Total Income : ₱{income:.2f}")
    print(f"  💸 Total Expense: ₱{expenses:.2f}")
    print(f"  🧾 Balance      : ₱{balance:.2f}\n")

def view_all_transactions():
    print("\n All Transactions")
    with open(FILENAME, newline="") as f:
        reader = list(csv.DictReader(f))
        if not reader:
            print(" No transactions found.\n")
            return

        for row in reader:
            print(f"{row['Date']} | {row['Type'].capitalize():<7} | ₱{float(row['Amount']):<8.2f} | {row['Category']:<10} | {row['Note']}")

        print("\n Last 5 Transactions")
        for row in reader[-5:]:
            print(f"{row['Date']} | {row['Type'].capitalize():<7} | ₱{float(row['Amount']):.2f} | {row['Category']:<10}")

        print()

def category_summary():
    totals = {}
    with open(FILENAME, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["Category"]
            amount = float(row["Amount"])
            totals[cat] = totals.get(cat, 0) + amount

    print("\n Spending by Category")
    if not totals:
        print(" No data to show.\n")
        return

    for cat, total in totals.items():
        print(f"  {cat:<12} : ₱{total:.2f}")
    print()

def reset_data():
    confirm = input(" Are you sure you want to clear all data? (yes/no): ").lower()
    if confirm == "yes":
        with open(FILENAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Amount", "Category", "Note"])
        print(" All data has been cleared.\n")
    else:
        print(" Reset cancelled.\n")

# Main Program Loop 

def main():
    while True:
        print("===== 📖 Personal Budget Tracker =====")
        print("1. ➕ Add Transaction")
        print("2. 📊 View Summary")
        print("3. 📋 View All Transactions")
        print("4. 📂 View Category Summary")
        print("5. 🔁 Reset All Data")
        print("6. ❌ Exit")
        choice = input("Choose option (1-6): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            reset_data()
        elif choice == "6":
            print(" Goodbye! Thank you for using the tracker.")
            break
        else:
            print(" Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
