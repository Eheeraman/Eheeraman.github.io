from expenses import Expense
import calendar
import datetime


def main():

    # User may adjust their montly budget as needed
    monthly_budget = 1000
    expenses_file_path = "expenses.csv"
    
    # Get user input
    expense = get_expense()
    
    # Put expenses into a file
    save__to_file(expense, expenses_file_path)
    
    # Read/summarize expenses
    give_summary(expenses_file_path, monthly_budget)


def get_expense():
    # gets input for expense name data
    expense_name = input("Enter expense name: ")

    # gets input for expense amount data
    expense_amnt = float(input("Enter expense amount: "))
    print(f"You've entered {expense_name}, {expense_amnt}")

    # List of categories to choose from
    expense_categories = ["Bills", "Food", "Work", "Fun", "Other"]

    # Gets the expense category and returns all input data when the selection is valid
    while True:
        print("Select an expense category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selection = int(input(f"Enter category number {value_range}: ")) - 1

        # returns data or asks for valid input if needed
        if selection in range(len(expense_categories)):
            selected_category = expense_categories[selection]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amnt
            )
            return new_expense
        else:
            print("Invalid category, please select another!")


def save__to_file(expense, expenses_file_path):
    print(f" Saving User Expense: {expense} to {expenses_file_path}")
    # saves data to csv file
    with open(expenses_file_path, "a") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")


def give_summary(expenses_file_path, budget):
    print("Expenses by Category: ")

    expenses: list[Expense] = []

    # making the categories as new ones are entered
    with open(expenses_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
  
            expense_name, expense_category, expense_amount = line.strip().split(",")

            line_expense = Expense(
                name=expense_name,
                category=expense_category,
                amount=float(expense_amount)
            )
            expenses.append(line_expense)

    category_amount = {}

    # adds to expenses for each category
    for expense in expenses:
        key = expense.category
        if key in category_amount:
            category_amount[key] += expense.amount
        else:
            category_amount[key] = expense.amount

    # shows the category and amount spent for each
    for key, amount in category_amount.items():
        print(f"    {key}:  ${amount:.2f}")

    # sums the entire list and shows total spent
    total_spent = sum([x.amount for x in expenses])
    print(f" You've spent ${total_spent:.2f} this month!")

    # shows budget remaining for the month
    remaining_budget = budget - total_spent
    print(f" You have ${remaining_budget:.2f} of your monthly budget remaining!")

    # Gets current date
    current_day = datetime.datetime.now()

    # Gets number of days in the current month
    days_in_month = calendar.monthrange(current_day.year, current_day.month)[1]

    #Calculate remaining days
    remaining_days = days_in_month - current_day.day

    # shows the daily budget for the rest of the month
    daily_budget = remaining_budget / remaining_days
    print(f" You're daily budget is now ${daily_budget:.2f}")


if __name__ == "__main__":
    # Runs only when ran directly
    main()
