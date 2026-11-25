from __future__ import annotations
import csv
import os


class StaffCsvManager:
    HEADERS = ["ID", "Name", "Salary"]

    def __init__(self, csv_path: str = "staff_records.csv"):
        self.csv_path = csv_path

    def _read_rows(self) -> list[list[str]] | None:
        if not os.path.exists(self.csv_path):
            print("CSV file not found. Initialize it first.")
            return None
        with open(self.csv_path, mode="r", newline="", encoding="utf-8") as fh:
            return list(csv.reader(fh))

    def _write_rows(self, rows: list[list[str]]) -> None:
        with open(self.csv_path, mode="w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(rows)

    def init_sheet(self) -> None:
        self._write_rows([self.HEADERS])
        print(f"Created {self.csv_path} with headers.")

    def insert_staff(self) -> None:
        rows = self._read_rows()
        if rows is None:
            return

        emp_id = input("Employee ID: ").strip()
        if not emp_id:
            print("ID cannot be blank.")
            return

        if any(r and r[0] == emp_id for r in rows[1:]):
            print(f"ID {emp_id} already exists.")
            return

        emp_name = input("Name: ").strip()
        try:
            emp_salary = int(input("Salary: ").strip())
        except ValueError:
            print("Salary must be a whole number.")
            return

        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow([emp_id, emp_name, emp_salary])
        print("Record saved.")

    def list_staff(self) -> None:
        rows = self._read_rows()
        if rows is None:
            return
        if len(rows) <= 1:
            print("No employee entries found.")
            return

        for r in rows:
            if len(r) >= 3:
                print(f"{r[0]:<8} {r[1]:<18} {r[2]}")

    def modify_staff(self) -> None:
        rows = self._read_rows()
        if not rows or len(rows) <= 1:
            if rows is not None:
                print("No employee entries found.")
            return

        target_id = input("Enter ID to edit: ").strip()
        for r in rows[1:]:
            if r and r[0] == target_id:
                new_name = input("New name: ").strip()
                try:
                    new_salary = int(input("New salary: ").strip())
                except ValueError:
                    print("Salary must be a whole number.")
                    return
                r[1] = new_name
                r[2] = str(new_salary)
                self._write_rows(rows)
                print("Record updated.")
                return

        print("No matching employee ID.")

    def remove_staff(self) -> None:
        rows = self._read_rows()
        if not rows or len(rows) <= 1:
            if rows is not None:
                print("No employee entries found.")
            return

        target_id = input("Enter ID to remove: ").strip()
        kept = [rows[0]] + [r for r in rows[1:] if r and r[0] != target_id]

        if len(kept) == len(rows):
            print("No matching employee ID.")
            return

        self._write_rows(kept)
        print("Record removed.")


def run_menu() -> None:
    store = StaffCsvManager()
    actions = {
        "1": store.init_sheet,
        "2": store.insert_staff,
        "3": store.list_staff,
        "4": store.modify_staff,
        "5": store.remove_staff,
    }

    while True:
        print("\n1. Create CSV  2. Add  3. View  4. Update  5. Delete  6. Exit")
        pick = input("Choice: ").strip()
        if pick == "6":
            break
        fn = actions.get(pick)
        if fn:
            fn()
        else:
            print("Enter a number between 1 and 6.")


if __name__ == "__main__":
    run_menu()
