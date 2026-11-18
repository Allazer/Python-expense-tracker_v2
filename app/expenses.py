from datetime import date, datetime
import math

DB_NAME = "expenses.db"

CATEGORIES = [
    "Food",
    "Clothing",
    "House Bills",
    "Entertainment",
    "Transport",
    "Misc"
]

def get_valid_date():
    while True:
        expense_date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if not expense_date:
            return date.today().isoformat()

        try:
            valid_date = datetime.strptime(
                expense_date, "%Y-%m-%d"
            )

            if valid_date.strftime("%Y-%m-%d") != expense_date:
                print("Please use YYYY-MM-DD format.")
                continue

            return expense_date

        except ValueError:
            print("Invalid date. Please enter a valid date.")

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter the amount!"))
            if math.isfinite(amount) and amount > 0:
                return amount
            else:
                print("The amount must be finite and greater than zero!")
        except ValueError:
            print("Enter a valid amount!")

def get_valid_description():
    while True:
            description = input("Enter your description!").strip()
            if description:
                return description
            else:
                print("Empty description")



def get_valid_category():
    while True:
        print(CATEGORIES)

        user_category = input("Choose your category").lower().strip()
        for category in CATEGORIES:
            if user_category == category.lower():
                return category
        else:
            print("Choose the correct category!")
       

def get_valid_expense_id():
    while True:
        try:
            expense_id = int(input("Enter your expense ID"))
            if expense_id > 0:
                return expense_id
            else:
                print("ID has to be greater than 0!!")
        except ValueError:
            print("Invalid expense ID!!")


# ---------------- CREATE ----------------

def add_expense():
    expense_date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not expense_date:
        expense_date = get_valid_date()

    category = get_valid_category()

    amount = get_valid_amount()
    
    description = get_valid_description()

    with connect_db() as connection:
        connection.execute("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """, (expense_date, category, amount, description))

    print("Expense added successfully!")


# ---------------- READ ----------------

def view_expenses():
    with connect_db() as connection:
        expenses = connection.execute("""
            SELECT * FROM expenses
            ORDER BY date DESC, id DESC
        """).fetchall()

    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Date | Category | Amount | Description")
    print("-" * 60)

    for expense in expenses:
        print(expense)


def search_expense():
    
    expense_id = get_valid_expense_id()
    
    with connect_db() as connection:
        expense = connection.execute("""
            SELECT * FROM expenses
            WHERE id = ?
        """, (expense_id,)).fetchone()

    if expense:
        print(expense)
    else:
        print("Expense not found.")


# ---------------- UPDATE ----------------

def update_expense():
    
    expense_id = get_valid_expense_id()
    
    new_category = get_valid_category()
  
    new_amount = get_valid_amount()

    new_description = get_valid_description()

    with connect_db() as connection:
        cursor = connection.execute("""
            UPDATE expenses
            SET category = ?, amount = ?, description = ?
            WHERE id = ?
        """, (new_category, new_amount,
              new_description, expense_id))

    if cursor.rowcount > 0:
        print("Expense updated successfully!")
    else:
        print("Expense ID not found.")


# ---------------- DELETE ----------------

def delete_expense():
   
    expense_id = get_valid_expense_id()
    

    with connect_db() as connection:
        expense = connection.execute("""
            SELECT * FROM expenses
            WHERE id = ?
        """, (expense_id,)).fetchone()

        if not expense:
            print("Expense not found.")
            return

        print("Selected expense:", expense)

        confirm = input("Are you sure you want to delete it? (yes/no): ")

        if confirm.lower() == "yes":
            connection.execute("""
                DELETE FROM expenses
                WHERE id = ?
            """, (expense_id,))

            print("Expense deleted successfully!")
        else:
            print("Deletion cancelled.")



