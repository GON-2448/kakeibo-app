from datetime import datetime
import sqlite3

def add_expense():

    date = input_date()

    item = input_item("項目を入力してください：")

    amount = input_amount()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (date, item, amount) VALUES (?, ?, ?)",
        (date, item, amount)
    )

    conn.commit()
    conn.close()

    print(f"{date} {item}：{amount}円を登録しました")

def show_expenses():
    print()
    print("===== 支出一覧 =====")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, item, amount FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()

    if not rows:
        print("支出データがありません")
    else:
        for row in rows:
            date = row[0]
            item = row[1]
            amount = row[2]

            print(f"{date} {item}：{amount}円")

    conn.close()
            
def show_total():
    total = 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT amount FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print()
        print("===== 合計金額 =====")
        print("支出データがありません")
        conn.close()
        return

    for row in rows:
        total += row[0]

    conn.close()

    print()
    print("===== 合計金額 =====")
    print(f"合計：{total}円")
    
def show_month_total():
    month = input("月を入力してください（例：2026-10）：")
    
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("月はYYYY-MM形式で入力してください")
        return

    total = 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM expenses WHERE date LIKE ?",
        (month + "%",)
    )

    rows = cursor.fetchall()

    if not rows:
        print()
        print(f"===== {month} の合計 =====")
        print("支出データがありません")
        conn.close()
        return

    for row in rows:
        total += row[0]

    conn.close()

    print()
    print(f"===== {month} の合計 =====")
    print(f"合計：{total}円")
    
def show_category_total():
    category_totals = {}

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT item, amount FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print()
        print("===== カテゴリ別合計 =====")
        print("支出データがありません")
        conn.close()
        return

    for row in rows:
        item = row[0]
        amount = row[1]

        if item in category_totals:
            category_totals[item] += amount
        else:
            category_totals[item] = amount

    conn.close()

    print()
    print("===== カテゴリ別合計 =====")

    for item, total in category_totals.items():
        print(f"{item}：{total}円")
        
def delete_expense():
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, date, item, amount FROM expenses")
    expenses = cursor.fetchall()

    print()
    print("===== 支出一覧 =====")
    
    if not expenses:
        print("支出データがありません")
        conn.close()
        return

    for i, row in enumerate(expenses, start=1):
        expense_id = row[0]
        date = row[1]
        item = row[2]
        amount = row[3]

        print(f"{i}. {date} {item}：{amount}円")

    
    delete_number = input_number(
        "削除する番号を入力してください：",
        len(expenses)
    )

    deleted = expenses[delete_number - 1]

    expense_id = deleted[0]

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    print(f"{deleted[1]} {deleted[2]}：{deleted[3]}円を削除しました")

    conn.close()

def edit_expense():
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, date, item, amount FROM expenses")
    expenses = cursor.fetchall()
    
    if not expenses:
        print("支出データがありません")
        conn.close()
        return

    print()
    print("===== 支出一覧 =====")

    for i, row in enumerate(expenses, start=1):
        expense_id = row[0]
        date = row[1]
        item = row[2]
        amount = row[3]

        print(f"{i}. {date} {item}：{amount}円")

    edit_number = input_number(
        "編集する番号を入力してください：",
        len(expenses)
    )

    new_date = input_date()

    new_item = input_item("新しい項目を入力してください：")

    print("新しい金額を入力します")
    new_amount = input_amount()

    edited = expenses[edit_number - 1]

    expense_id = edited[0]

    cursor.execute(
        """
        UPDATE expenses
        SET date = ?, item = ?, amount = ?
        WHERE id = ?
        """,
        (new_date, new_item, new_amount, expense_id)
    )

    conn.commit()
    conn.close()

    print(f"{new_date} {new_item}：{new_amount}円に更新しました")
    
import sqlite3


def get_connection():
    return sqlite3.connect("kakeibo.db")

def input_amount():
    while True:
        try:
            amount = int(input("金額を入力してください："))
        except ValueError:
            print("金額は数字で入力してください")
            continue

        if amount <= 0:
            print("金額は1円以上で入力してください")
            continue

        return amount
    
def input_date():
    while True:
        date = input("日付を入力してください（例：2026-10-05）：")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("日付はYYYY-MM-DD形式で入力してください")
            
def input_number(message, max_number):
    while True:
        try:
            number = int(input(message))
        except ValueError:
            print("番号は数字で入力してください")
            continue

        if number < 1 or number > max_number:
            print("正しい番号を入力してください")
            continue

        return number
    
def input_item(message):
    while True:
        item = input(message).strip()

        if not item:
            print("項目を入力してください")
            continue

        return item

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            item TEXT,
            amount INTEGER
        )
    """)

    conn.commit()
    conn.close()

def main():
    init_db()
    while True:
        print()
        print("===== 家計簿 =====")
        print("1. 支出を登録")
        print("2. 支出一覧を見る")
        print("3. 合計を見る")
        print("4. 月ごとの合計を見る")
        print("5. カテゴリ別の合計を見る")
        print("6. 支出を削除")
        print("7. 支出を編集")
        print("8. 終了")

        choice = input("番号を選択してください：")

        if choice == "1":
            add_expense()

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            show_total()

        elif choice == "4":
            show_month_total()

        elif choice == "5":
            show_category_total()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
            edit_expense()

        elif choice == "8":
            print("家計簿を終了します")
            break

    else:
        print("1～8を入力してください")
        
if __name__ == "__main__":
    main()
        