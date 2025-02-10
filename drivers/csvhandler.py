import os
import csv
from typing import Dict, List, Union, Any


class CSVHandler:
    """A class to handle CSV file operations including checking existence, writing, updating, and reading CSV data."""

    def __init__(self, file_path: str, fieldnames: List[str]):
        """
        Initializes the CSVHandler.

        :param file_path: Path to the CSV file.
        :param fieldnames: List of column names for the CSV.
        """
        self.file_path = file_path
        self.fieldnames = fieldnames
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensures that the CSV file exists; if not, creates it with headers."""
        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def save_dict_to_csv(self, data: Dict[str, Union[str, int, float]]) -> None:
        """
        Saves a single dictionary as a row in the CSV file.

        :param data: A dictionary containing row data.
        :raises ValueError: If dictionary keys do not match fieldnames.
        """
        if set(data.keys()) != set(self.fieldnames):
            raise ValueError("Dictionary keys must match CSV fieldnames.")

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(data)

    def save_list_to_csv(
        self, data_list: List[Dict[str, Union[str, int, float]]]
    ) -> None:
        """
        Saves a list of dictionaries to the CSV file.

        :param data_list: A list of dictionaries, where each dictionary represents a row.
        :raises ValueError: If any dictionary keys do not match fieldnames.
        """
        if not data_list:
            return  # No data to write

        if any(set(row.keys()) != set(self.fieldnames) for row in data_list):
            raise ValueError("All dictionary keys must match CSV fieldnames.")

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerows(data_list)  # Write multiple rows at once

    def update_csv_row(
        self, unique_column: str, unique_value: Any, updates: Dict[str, Any]
    ) -> bool:
        """
        Updates specific columns of a CSV row based on a unique column value.

        :param unique_column: The column to search for the unique value.
        :param unique_value: The value that identifies the row to update.
        :param updates: A dictionary with column names as keys and new values.
        :return: True if an update was made, False otherwise.
        :raises ValueError: If unique_column or update keys are not in fieldnames.
        """
        if unique_column not in self.fieldnames:
            raise ValueError(f"Column '{unique_column}' is not in CSV fieldnames.")

        if any(col not in self.fieldnames for col in updates.keys()):
            raise ValueError("Some update keys do not match CSV fieldnames.")

        updated = False
        rows = []

        # Read the existing CSV data
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[unique_column] == str(
                    unique_value
                ):  # Convert to string for consistency
                    row.update(updates)  # Apply updates
                    updated = True
                rows.append(row)

        # Write updated data back to the CSV
        if updated:
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        return updated

    def read_csv(self) -> List[Dict[str, Any]]:
        """
        Reads the CSV file and returns a list of dictionaries representing each row.

        :return: A list of dictionaries where each dictionary is a row in the CSV file.
        """
        data = []
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(dict(row))  # Convert OrderedDict to a regular dict
        return data


# Example usage
if __name__ == "__main__":
    csv_file = "data.csv"
    columns = ["id", "name", "age"]

    csv_handler = CSVHandler(csv_file, columns)

    # Add a single row
    sample_data = {"id": "1", "name": "Alice", "age": "30"}
    csv_handler.save_dict_to_csv(sample_data)

    # Add multiple rows
    sample_list = [
        {"id": "2", "name": "Bob", "age": "25"},
        {"id": "3", "name": "Charlie", "age": "40"},
    ]
    csv_handler.save_list_to_csv(sample_list)

    # Update a specific row
    updated = csv_handler.update_csv_row("id", "1", {"age": "31"})
    if updated:
        print("CSV row updated successfully!")
    else:
        print("No matching row found to update.")

    # Read and print the CSV contents
    print("\nCSV Contents:")
    rows = csv_handler.read_csv()
    for row in rows:
        print(row)
