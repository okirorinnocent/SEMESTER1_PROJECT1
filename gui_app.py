"""
    STUDENT PERFORMANCE MANAGEMENT SYSTEM - DESKTOP GUI
    Author: Okiror Innocent
    Institution: Mbarara University of Science and Technology (MUST)
"""

import tkinter as tk
from tkinter import messagebox, ttk
from dataclasses import dataclass


@dataclass
class Course:
    code: str
    credits: int
    score: float
    gp: float
    letter: str


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


class GPACalculatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MUST Student Performance Management System")
        self.root.geometry("650x600")
        self.root.resizable(False, False)

        self.courses: list[Course] = []

        # Application Title Header
        title_label = tk.Label(
            root,
            text="MUST SEMESTER GPA CALCULATOR",
            font=("Helvetica", 14, "bold"),
            bg="#003366",
            fg="white",
            padding=10
        )
        title_label.pack(fill=tk.X)

        # Student Details Frame
        student_frame = ttk.LabelFrame(
            root, text=" Student Details ", padding=10)
        student_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(student_frame, text="Student Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.entry_name = ttk.Entry(student_frame, width=40)
        self.entry_name.grid(row=0, column=1, pady=5)

        # Course Entry Frame
        course_frame = ttk.LabelFrame(root, text=" Add Course ", padding=10)
        course_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Label(course_frame, text="Course Code:").grid(
            row=0, column=0, sticky=tk.W, padx=5)
        self.entry_code = ttk.Entry(course_frame, width=10)
        self.entry_code.grid(row=0, column=1, padx=5)

        ttk.Label(course_frame, text="Credit Units:").grid(
            row=0, column=2, sticky=tk.W, padx=5)
        self.entry_credits = ttk.Entry(course_frame, width=6)
        self.entry_credits.grid(row=0, column=3, padx=5)

        ttk.Label(course_frame, text="Score (%):").grid(
            row=0, column=4, sticky=tk.W, padx=5)
        self.entry_score = ttk.Entry(course_frame, width=6)
        self.entry_score.grid(row=0, column=5, padx=5)

        btn_add = ttk.Button(
            course_frame, text="Add Course", command=self.add_course)
        btn_add.grid(row=0, column=6, padx=10)

        # Course Table View
        table_frame = ttk.LabelFrame(root, text=" Added Courses ", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("code", "credits", "score", "grade", "gp")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8)
        self.tree.heading("code", text="Course Code")
        self.tree.heading("credits", text="Credits")
        self.tree.heading("score", text="Score (%)")
        self.tree.heading("grade", text="Letter Grade")
        self.tree.heading("gp", text="Grade Point")

        self.tree.column("code", width=120, anchor=tk.CENTER)
        self.tree.column("credits", width=80, anchor=tk.CENTER)
        self.tree.column("score", width=100, anchor=tk.CENTER)
        self.tree.column("grade", width=100, anchor=tk.CENTER)
        self.tree.column("gp", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Calculate Button & Summary Frame
        bottom_frame = ttk.Frame(root, padding=10)
        bottom_frame.pack(fill=tk.X, padx=15)

        btn_calc = tk.Button(
            bottom_frame,
            text="Calculate GPA",
            font=("Helvetica", 10, "bold"),
            bg="#28a745",
            fg="white",
            command=self.calculate_gpa
        )
        btn_calc.pack(side=tk.LEFT, padx=5)

        btn_reset = tk.Button(
            bottom_frame,
            text="Reset",
            bg="#dc3545",
            fg="white",
            command=self.reset_all
        )
        btn_reset.pack(side=tk.LEFT, padx=5)

        self.lbl_result = ttk.Label(
            bottom_frame,
            text="Semester GPA: -- / 5.00",
            font=("Helvetica", 11, "bold")
        )
        self.lbl_result.pack(side=tk.RIGHT, padx=10)

    def add_course(self):
        code = self.entry_code.get().strip().upper()
        credits_str = self.entry_credits.get().strip()
        score_str = self.entry_score.get().strip()

        if not code or not credits_str or not score_str:
            messagebox.showerror("Error", "Please fill in all course fields.")
            return

        try:
            credits = int(credits_str)
            if credits < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Credit units must be a whole number (at least 1).")
            return

        try:
            score = float(score_str)
            if not (0 <= score <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Score must be a number between 0 and 100.")
            return

        gp, letter = calculate_grade_point(score)
        course = Course(code=code, credits=credits,
                        score=score, gp=gp, letter=letter)
        self.courses.append(course)

        # Insert row into display table
        self.tree.insert("", tk.END, values=(
            code, credits, f"{score:.1f}", letter, f"{gp:.1f}"))

        # Clear inputs for next course
        self.entry_code.delete(0, tk.END)
        self.entry_credits.delete(0, tk.END)
        self.entry_score.delete(0, tk.END)

    def calculate_gpa(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror(
                "Error", "Please enter the student's full name.")
            return

        if not self.courses:
            messagebox.showerror("Error", "Please add at least one course.")
            return

        total_credits = sum(c.credits for c in self.courses)
        total_weighted_gp = sum(c.gp * c.credits for c in self.courses)
        gpa = total_weighted_gp / total_credits if total_credits > 0 else 0.0

        self.lbl_result.config(text=f"Semester GPA: {gpa:.2f} / 5.00")
        messagebox.showinfo(
            "Academic Summary",
            f"Student: {name.upper()}\n"
            f"Total Credit Units: {total_credits}\n"
            f"Final Semester GPA: {gpa:.2f} / 5.00"
        )

    def reset_all(self):
        self.courses.clear()
        self.entry_name.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)
        self.entry_credits.delete(0, tk.END)
        self.entry_score.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.lbl_result.config(text="Semester GPA: -- / 5.00")


if __name__ == "__main__":
    root = tk.Tk()
    app = GPACalculatorGUI(root)
    root.mainloop()
