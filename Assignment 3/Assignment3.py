import sqlite3


class StaffDatabase:
    def __init__(self, db_path: str = "company_staff.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INTEGER PRIMARY KEY,
                emp_name TEXT NOT NULL,
                emp_salary INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def insert_row(self) -> None:
        try:
            emp_id = int(input("Employee ID: ").strip())
            emp_name = input("Name: ").strip()
            emp_salary = int(input("Salary: ").strip())
        except ValueError:
            print("ID and salary must be integers.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO employee (emp_id, emp_name, emp_salary) VALUES (?, ?, ?)",
                (emp_id, emp_name, emp_salary),
            )
            self.conn.commit()
            print("Employee added.")
        except sqlite3.IntegrityError:
            print(f"Employee ID {emp_id} already exists.")

    def fetch_all(self) -> None:
        self.cursor.execute(
            "SELECT emp_id, emp_name, emp_salary FROM employee ORDER BY emp_id"
        )
        records = self.cursor.fetchall()
        if not records:
            print("Employee table is empty.")
            return

        print(f"{'ID':<6} {'Name':<18} {'Salary'}")
        for emp_id, emp_name, emp_salary in records:
            print(f"{emp_id:<6} {emp_name:<18} {emp_salary}")

    def change_salary(self) -> None:
        try:
            emp_id = int(input("Employee ID to update: ").strip())
            new_salary = int(input("New salary: ").strip())
        except ValueError:
            print("ID and salary must be integers.")
            return

        self.cursor.execute(
            "UPDATE employee SET emp_salary = ? WHERE emp_id = ?",
            (new_salary, emp_id),
        )
        self.conn.commit()
        if self.cursor.rowcount == 0:
            print("No matching employee ID.")
        else:
            print("Salary updated.")

    def delete_row(self) -> None:
        try:
            emp_id = int(input("Employee ID to delete: ").strip())
        except ValueError:
            print("ID must be an integer.")
            return

        self.cursor.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            print("No matching employee ID.")
        else:
            print("Employee deleted.")

    def close(self) -> None:
        self.conn.close()


def main() -> None:
    db = StaffDatabase()
    menu = {
        "1": db.insert_row,
        "2": db.fetch_all,
        "3": db.change_salary,
        "4": db.delete_row,
    }

    try:
        while True:
            print("\n1. Add  2. Display  3. Update Salary  4. Delete  5. Exit")
            opt = input("Select option: ").strip()
            if opt == "5":
                break
            handler = menu.get(opt)
            if handler:
                handler()
            else:
                print("Choose a valid option (1-5).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
