from tabulate import tabulate
import pandas as pd
from datetime import date
import mariadb
import sys
from IPython.display import display

def read_query(conn, query):
    cur=conn.cursor()
    result = None
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except mariadb.Error as err:
        print(f'Error: "{err}"')


def print_query(conn, query):
    db=[]
    results = read_query(conn, query)
    for result in results:
        result = list(result)
        db.append(result)
    columns = ["SNO", "DATE", "EXPENSE", "REASON"]
    df = pd.DataFrame(db, columns=columns)
    print("--------------------------------------------------------------")
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print("----------XX---------------XX-------------------XX------------")

def print_expense_query(conn, query):
    db=[]
    results = read_query(conn, query)
    for result in results:
        result = list(result)
        db.append(result)
    columns = ["TOTAL EXPENSE"]
    df = pd.DataFrame(db, columns=columns)
    print("----------XX---------------XX-------------------XX------------")
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print('--------------------------------------------------------------')


#CONNECTION

try:
    conn = mariadb.connect(
        user = "hari",
        password = "hari",
        host = "127.0.0.1",
        port = 3306,
        database = "budgetdb"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB : {e}")
    sys.exit(1)

print("----------------------------------")
print("         MyBudget                 ")
print("----------------------------------")
print("1. Add expense")
print("2. View total expense\n")
choice = input()

cur = conn.cursor()

#new table = create table budget (sno int not null auto_increment primary key, exp_date date, expense int, reason varchar(50));"
if (choice == "1"):
    date = input("\nEnter date in yyyy-mm-dd\n")
    expense = input("Enter amount\n")
    reason = input("Enter reason\n")
    query = "insert into budget(exp_date, expense, reason) values (%s,%s,%s);"
    data = (date, expense, reason)
    cur.execute(query,data)
    conn.commit()
    
elif (choice == "2"):
    print("\n1. Total expenditure of a specific month")
    print("2. Total expenditure of a specific day")
    print("3. Grand total")
    user_choice = input("\nWhat do you need\n")

    if user_choice == "1":
        user_month = input("\nEnter month\n")
        query = "select * from budget where monthname(exp_date)='"+user_month+"';"
        print_query(conn, query)

        query = "select sum(expense) from budget where monthname(exp_date)='" + user_month + "';"
        print_expense_query(conn, query)

    elif user_choice == '2':
        specific_day = input("\nEnter the date in yyyy-mm-dd\n")
        query = "select * from budget where exp_date ='" + specific_day +"';"
        print_query(conn, query)
        
        query ="select sum(expense) from budget where exp_date ='" + specific_day +"';"
        print_expense_query(conn, query)

    elif user_choice == '3':
        query ="select * from budget;"
        print_query(conn, query)
        
        query = "select sum(expense) from budget;"
        print_expense_query(conn, query)