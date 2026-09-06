"""
    STUDENT PERFORMANCE MANAGEMENT SYSTEM - RICH TERMINAL UI
    Author: Okiror Innocent
    Institution: Mbarara University of Science and Technology (MUST)
"""

from dataclasses import dataclass
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt, InvalidResponse

console = Console()


@dataclass
class Course:
    code: str
    credits: int
    score: float
    gp: float
    letter: str


def calculate_grade_point(score: float) -> tuple[float, str]:
    """Translates a raw score percentage into MUST Grade Points and Letter Grade."""
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


def get_non_empty_prompt(prompt_text: str) -> str:
    """Ensures input is not empty or just whitespace."""
    while True:
        value = Prompt.ask(prompt_text).strip()
        if value:
            return value
        console.print(
            "[bold red][!] Input cannot be empty. Please try again.[/bold red]")


def main() -> None:
    console.print(
        Panel.fit(
            "[bold white]UNIVERSITY SEMESTER ACADEMIC PERFORMANCE CALCULATOR[/bold white]\n"
            "[italic cyan]Mbarara University of Science and Technology[/italic cyan]",
            style="blue",
        )
    )

    try:
        # Prompt for student details with non-empty validation
        student_name = get_non_empty_prompt(
            "\n[bold yellow]Enter Student Full Name[/bold yellow]")

        # Prompt for total course count (minimum 1)
        while True:
            try:
                course_count = IntPrompt.ask(
                    "[bold yellow]Enter number of courses taken[/bold yellow]", default=1)
                if course_count >= 1:
                    break
                console.print(
                    "[bold red][!] Number of courses must be at least 1.[/bold red]")
            except InvalidResponse:
                console.print(
                    "[bold red][!] Invalid input. Please enter a valid whole number.[/bold red]")

        courses: list[Course] = []
        total_credit_units = 0
        total_weighted_points = 0.0

        for i in range(1, course_count + 1):
            console.rule(f"[bold green]Course {i} Entry[/bold green]")

            code = get_non_empty_prompt("Course Code").upper()

            # Ensure credit units are at least 1
            while True:
                try:
                    credits = IntPrompt.ask("Credit Units")
                    if credits >= 1:
                        break
                    console.print(
                        "[bold red][!] Credit units must be at least 1.[/bold red]")
                except InvalidResponse:
                    console.print(
                        "[bold red][!] Invalid input. Please enter a valid integer for credit units.[/bold red]")

            # Ensure score percentage is between 0 and 100
            while True:
                try:
                    score = FloatPrompt.ask("Final Score Percentage (0-100)")
                    if 0 <= score <= 100:
                        break
                    console.print(
                        "[bold red][!] Score must be between 0 and 100.[/bold red]")
                except InvalidResponse:
                    console.print(
                        "[bold red][!] Invalid input. Please enter a valid number for score.[/bold red]")

            gp, letter = calculate_grade_point(score)
            total_credit_units += credits
            total_weighted_points += gp * credits

            courses.append(
                Course(
                    code=code,
                    credits=credits,
                    score=score,
                    gp=gp,
                    letter=letter,
                )
            )

        # Calculate weighted GPA
        gpa = total_weighted_points / total_credit_units if total_credit_units > 0 else 0.0

        # Render Summary Table
        table = Table(
            title=f"\n[bold magenta]ACADEMIC SUMMARY FOR: {student_name.upper()}[/bold magenta]"
        )
        table.add_column("Course Code", style="cyan", justify="center")
        table.add_column("Credits", style="magenta", justify="center")
        table.add_column("Score (%)", style="green", justify="center")
        table.add_column("Letter Grade", style="bold yellow", justify="center")
        table.add_column("Grade Point", style="blue", justify="center")

        for c in courses:
            table.add_row(
                c.code,
                str(c.credits),
                f"{c.score:.1f}",
                c.letter,
                f"{c.gp:.1f}",
            )

        console.print(table)
        console.print(
            f"\n[bold]Total Credit Units Accumulated:[/bold] [cyan]{total_credit_units}[/cyan]")
        console.print(
            f"[bold]Final Semester GPA:[/bold] [bold green]{gpa:.2f} / 5.00[/bold green]\n")

    except KeyboardInterrupt:
        console.print(
            "\n\n[bold red][!] Operation cancelled by user. Exiting...[/bold red]")
        sys.exit(0)


if __name__ == "__main__":
    main()
