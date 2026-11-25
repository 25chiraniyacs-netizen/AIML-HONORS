from __future__ import annotations
import os
import sqlite3
import pandas as pd


class EmployeePandasStore:
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "company_payroll.db"
            )
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INTEGER PRIMARY KEY,
                emp_name TEXT NOT NULL,
                emp_salary INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_member(self) -> None:
        try:
            emp_id = int(input("Employee ID: ").strip())
            emp_name = input("Name: ").strip()
            emp_salary = int(input("Salary: ").strip())
        except ValueError:
            print("ID and salary must be integers.")
            return

        existing = pd.read_sql_query(
            "SELECT emp_id FROM employee WHERE emp_id = ?",
            self.conn,
            params=(emp_id,),
        )
        if not existing.empty:
            print(f"Employee ID {emp_id} already exists.")
            return

        row_df = pd.DataFrame(
            [{"emp_id": emp_id, "emp_name": emp_name, "emp_salary": emp_salary}]
        )
        row_df.to_sql("employee", self.conn, if_exists="append", index=False)
        print("Employee added.")

    def view_table(self) -> None:
        df = pd.read_sql_query(
            "SELECT emp_id, emp_name, emp_salary FROM employee ORDER BY emp_id",
            self.conn,
        )
        if df.empty:
            print("No employee rows stored.")
            return
        print(df.to_string(index=False))

    def modify_salary(self) -> None:
        try:
            emp_id = int(input("Employee ID to update: ").strip())
            new_salary = int(input("New salary: ").strip())
        except ValueError:
            print("ID and salary must be integers.")
            return

        cur = self.conn.execute(
            "UPDATE employee SET emp_salary = ? WHERE emp_id = ?",
            (new_salary, emp_id),
        )
        self.conn.commit()
        if cur.rowcount == 0:
            print("No matching employee ID.")
        else:
            print("Salary updated.")

    def remove_member(self) -> None:
        try:
            emp_id = int(input("Employee ID to remove: ").strip())
        except ValueError:
            print("ID must be an integer.")
            return

        cur = self.conn.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
        self.conn.commit()
        if cur.rowcount == 0:
            print("No matching employee ID.")
        else:
            print("Employee removed.")

    def close(self) -> None:
        self.conn.close()


def run_cli() -> None:
    store = EmployeePandasStore()
    options = {
        "1": store.add_member,
        "2": store.view_table,
        "3": store.modify_salary,
        "4": store.remove_member,
    }

    try:
        while True:
            print("\n1. Add  2. View  3. Update Salary  4. Delete  5. Exit")
            pick = input("Choice: ").strip()
            if pick == "5":
                break
            fn = options.get(pick)
            if fn:
                fn()
            else:
                print("Enter a valid option (1-5).")
    finally:
        store.close()


if __name__ == "__main__":
    run_cli()
