"""
    STUDENT PERFORMANCE MANAGEMENT SYSTEM - RICH TERMINAL UI
    Author: Okiror Innocent
    Institution: Mbarara University of Science and Technology (MUST)
"""

from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt

console = Console()


@dataclass
class Course:
    code: str
    credits: int
    score: float
    gp: float
    letter: str


def calculate_grade_point(score: float) -> tuple[float, str]:
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


def main():
    console.print(
        Panel.fit(
            "[bold white]UNIVERSITY SEMESTER ACADEMIC PERFORMANCE CALCULATOR[/bold white]\n"
            "[italic cyan]Mbarara University of Science and Technology[/italic cyan]",
            style="blue"
        )
    )

    student_name = Prompt.ask(
        "\n[bold yellow]Enter Student Full Name[/bold yellow]")
    course_count = IntPrompt.ask(
        "[bold yellow]Enter number of courses taken[/bold yellow]", default=1)

    courses: list[Course] = []
    total_credit_units = 0
    total_weighted_points = 0.0

    for i in range(1, course_count + 1):
        console.rule(f"[bold green]Course {i} Entry[/bold green]")
        code = Prompt.ask("Course Code").upper()
        credits = IntPrompt.ask("Credit Units")

        while True:
            score = FloatPrompt.ask("Final Score Percentage (0-100)")
            if 0 <= score <= 100:
                break
            console.print(
                "[bold red][!] Score must be between 0 and 100.[/bold red]")

        gp, letter = calculate_grade_point(score)
        total_credit_units += credits
        total_weighted_points += gp * credits

        courses.append(Course(code=code, credits=credits,
                       score=score, gp=gp, letter=letter))

    gpa = total_weighted_points / total_credit_units if total_credit_units > 0 else 0.0

    # Render Summary Table
    table = Table(
        title=f"\n[bold magenta]ACADEMIC SUMMARY FOR: {student_name.upper()}[/bold magenta]")
    table.add_column("Course Code", style="cyan", justify="center")
    table.add_column("Credits", style="magenta", justify="center")
    table.add_column("Score (%)", style="green", justify="center")
    table.add_column("Letter Grade", style="bold yellow", justify="center")
    table.add_column("Grade Point", style="blue", justify="center")

    for c in courses:
        table.add_row(c.code, str(c.credits),
                      f"{c.score:.1f}", c.letter, f"{c.gp:.1f}")

    console.print(table)
    console.print(
        f"\n[bold]Total Credit Units Accumulated:[/bold] [cyan]{total_credit_units}[/cyan]")
    console.print(
        f"[bold]Final Semester GPA:[/bold] [bold green]{gpa:.2f} / 5.00[/bold green]\n")


if __name__ == "__main__":
    main()
