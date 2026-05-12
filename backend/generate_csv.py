import argparse
import csv
import random
from dataclasses import dataclass


FIELDNAMES = [
    "patient_first_name",
    "patient_last_name",
    "email",
    "doctor_name",
    "specialization",
    "status",
    "report_text",
    "study_file_name",
]

FIRST_NAMES = [
    "Alex",
    "Olivia",
    "Noah",
    "Emma",
    "Liam",
    "Mia",
    "Ethan",
    "Ava",
    "Lucas",
    "Sofia",
]

LAST_NAMES = [
    "Johnson",
    "Brown",
    "Taylor",
    "Miller",
    "Davis",
    "Anderson",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
]

DOCTORS = [
    "Dr. Carter",
    "Dr. Wright",
    "Dr. Lewis",
    "Dr. Walker",
    "Dr. Harris",
]

SPECIALIZATIONS = [
    "Oncology",
    "Radiology",
    "Pathology",
    "Surgery",
    "Therapy",
]

STATUSES = [
    "new",
    "in_review",
    "confirmed",
    "archived",
]

REPORT_SNIPPETS = [
    "Routine screening report",
    "Follow-up requested",
    "No anomalies detected",
    "Secondary review required",
    "Imaging data attached",
]


@dataclass
class CsvGenerator:
    rows: int

    def generate(self, file_path: str) -> None:
        with open(file_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            writer.writeheader()
            for index in range(1, self.rows + 1):
                writer.writerow(self._build_row(index))

    def _build_row(self, index: int) -> dict[str, str]:
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{index}@example.com"
        report_text = f"{random.choice(REPORT_SNIPPETS)} #{index}"
        return {
            "patient_first_name": first_name,
            "patient_last_name": last_name,
            "email": email,
            "doctor_name": random.choice(DOCTORS),
            "specialization": random.choice(SPECIALIZATIONS),
            "status": random.choice(STATUSES),
            "report_text": report_text,
            "study_file_name": f"study_{index:05d}.txt",
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        default="posts.csv",
        help="Path to output CSV file",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=1000,
        help="Number of rows to generate (min 1000)",
    )
    args = parser.parse_args()

    rows = max(args.rows, 1000)
    generator = CsvGenerator(rows=rows)
    generator.generate(args.out)
    print(f"Generated rows: {rows} -> {args.out}")


if __name__ == "__main__":
    main()
