"""
    STUDENT PERFORMANCE MANAGEMENT SYSTEM
    Semester GPA Calculator
    
    Author: Okiror Innocent
    EMPLOYMENT: COMPUTER SCIENCE STUDENT
    Institution: Mbarara University of Science and Technology (MUST)
    Description: Lightweight command-line tool to calculate semester GPA based on 
                 the university grading scale.
"""

from dataclasses import dataclass
import sys


@dataclass
class Course:
    """Represents an academic course module."""
    code: str
    credits: int
    score: float
    gp: float
    letter: str


def get_valid_string(prompt: str) -> str:
    """Prompts for a string and ensures non-empty input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[!] Input cannot be empty. Please try again.")


def get_valid_float(prompt: str, min_val: float, max_val: float) -> float:
    """Prompts for a floating-point number and validates its range."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")
            continue

        if min_val <= value <= max_val:
            return value
        print(f"[!] Input must be between {min_val} and {max_val}.")


def get_valid_int(prompt: str, min_val: int = 1) -> int:
    """Prompts for an integer and ensures it meets a minimum threshold."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("[!] Invalid input. Please enter a whole integer.")
            continue

        if value >= min_val:
            return value
        print(f"[!] Number must be at least {min_val}.")


def calculate_grade_point(score: float) -> tuple[float, str]:
    """Translates a raw score percentage into Grade Points and Letter Grade."""
    if score >= 80.0:
        return 5.0, "A"
    if score >= 75.0:
        return 4.5, "B+"
    if score >= 70.0:
        return 4.0, "B"
    if score >= 65.0:
        return 3.5, "C+"
    if score >= 60.0:
        return 3.0, "C"
    if score >= 55.0:
        return 2.5, "D+"
    if score >= 50.0:
        return 2.0, "D"
    return 0.0, "F"


def main() -> None:
    print("=====================================================")
    print(" UNIVERSITY SEMESTER ACADEMIC PERFORMANCE CALCULATOR")
    print("=====================================================\n")

    try:
        student_name = get_valid_string("Enter Student Full Name: ")
        course_count = get_valid_int(
            "Enter number of courses taken this semester: "
        )

        courses: list[Course] = []
        total_credit_units = 0
        total_weighted_points = 0.0

        for course_number in range(1, course_count + 1):
            print(f"\n--- Course {course_number} Entry ---")
            code = get_valid_string("Course Code (e.g., CS1101): ").upper()
            credit_units = get_valid_int("Credit units: ", min_val=1)
            score = get_valid_float(
                "Final Score Percentage (0-100): ", min_val=0.0, max_val=100.0
            )

            grade_point, letter = calculate_grade_point(score)

            total_credit_units += credit_units
            total_weighted_points += grade_point * credit_units

            courses.append(
                Course(
                    code=code,
                    credits=credit_units,
                    score=score,
                    gp=grade_point,
                    letter=letter,
                )
            )

        # Calculate credit-weighted GPA
        gpa = total_weighted_points / total_credit_units if total_credit_units > 0 else 0.0

        # Display the formatted summary
        print("\n" + "=" * 60)
        print(f"ACADEMIC SUMMARY FOR: {student_name.upper()}")
        print("=" * 60)
        print(f"{'CODE':<10} | {'CREDITS':<8} | {'SCORE':<10} | {'GRADE':<6} | GP")
        print("-" * 60)
        for course in courses:
            print(
                f"{course.code:<10} | {course.credits:<8} | "
                f"{course.score:<10.1f} | {course.letter:<6} | {course.gp:.1f}"
            )
        print("-" * 60)
        print(f"Total Credit Units : {total_credit_units}")
        print(f"Semester GPA       : {gpa:.2f}/5.00")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user. Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
