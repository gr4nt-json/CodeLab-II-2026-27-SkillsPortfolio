"""
Student Manager Application - Exercise 3
CodeLab II Programming Skills Portfolio

Acknowledgement: The Tkinter Text widget formatting, simpledialog integration, 
and file rewriting logic were developed with the assistance of Qwen (Generative AI). 
Prompt used: "Create a Tkinter class that manages a list of dictionaries loaded 
from a CSV-style text file, performs calculations, and rewrites the file on update."
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("700x600")
        
        self.file_path = "studentMarks.txt"
        self.students = []
        
        self.load_data()
        self.setup_ui()

    def setup_ui(self):
        """Builds the main interface."""
        tk.Label(self.root, text="Student Manager System", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Output area
        self.output_text = tk.Text(self.root, height=20, width=80, font=("Consolas", 11), state=tk.DISABLED)
        self.output_text.pack(pady=10, padx=10)
        
        # Button frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Base Requirements (1-4)
        tk.Button(btn_frame, text="1. View All Records", command=self.view_all, width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="2. View Individual", command=self.view_individual, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="3. Highest Mark", command=self.view_highest, width=20).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="4. Lowest Mark", command=self.view_lowest, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Extensions (5-8)
        tk.Button(btn_frame, text="5. Sort Records", command=self.sort_records, width=20).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="6. Add Student", command=self.add_student, width=20).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="7. Delete Student", command=self.delete_student, width=20).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="8. Update Student", command=self.update_student, width=20).grid(row=3, column=1, padx=5, pady=5)

    def load_data(self):
        """Reads studentMarks.txt and parses into a list of dictionaries."""
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                # Skip first line (student count)
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        self.students.append({
                            'code': parts[0],
                            'name': parts[1],
                            'cw1': int(parts[2]),
                            'cw2': int(parts[3]),
                            'cw3': int(parts[4]),
                            'exam': int(parts[5])
                        })
        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt not found.")

    def save_data(self):
        """Writes the current student list back to the file."""
        with open(self.file_path, 'w') as f:
            f.write(f"{len(self.students)}\n")
            for s in self.students:
                f.write(f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")

    def calculate_stats(self, student):
        """Calculates total coursework, total marks, percentage, and grade."""
        total_cw = student['cw1'] + student['cw2'] + student['cw3']
        total_marks = total_cw + student['exam']
        percentage = (total_marks / 160) * 100
        
        if percentage >= 70: grade = 'A'
        elif percentage >= 60: grade = 'B'
        elif percentage >= 50: grade = 'C'
        elif percentage >= 40: grade = 'D'
        else: grade = 'F'
        
        return total_cw, total_marks, percentage, grade

    def format_student(self, student):
        """Formats a student dictionary into a display string."""
        cw, total, pct, grade = self.calculate_stats(student)
        return (f"Name: {student['name']}\n"
                f"Code: {student['code']}\n"
                f"Coursework: {cw}/60 | Exam: {student['exam']}/100\n"
                f"Total: {total}/160 ({pct:.1f}%) - Grade: {grade}\n"
                f"{'-'*40}")

    def display_output(self, text):
        """Clears and updates the Text widget."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    # --- Menu Functions ---

    def view_all(self):
        if not self.students:
            self.display_output("No records found.")
            return
            
        output = "=== ALL STUDENT RECORDS ===\n\n"
        total_pct = 0
        for s in self.students:
            output += self.format_student(s) + "\n"
            total_pct += self.calculate_stats(s)[2]
            
        avg_pct = total_pct / len(self.students)
        output += f"\n=== CLASS SUMMARY ===\nTotal Students: {len(self.students)}\nAverage Percentage: {avg_pct:.1f}%"
        self.display_output(output)

    def view_individual(self):
        code = simpledialog.askstring("Input", "Enter Student Code:")
        if code:
            student = next((s for s in self.students if s['code'] == code), None)
            if student:
                self.display_output("=== INDIVIDUAL RECORD ===\n\n" + self.format_student(student))
            else:
                messagebox.showinfo("Not Found", "Student code not found.")

    def view_highest(self):
        if not self.students: return
        best = max(self.students, key=lambda s: self.calculate_stats(s)[1])
        self.display_output("=== HIGHEST MARK ===\n\n" + self.format_student(best))

    def view_lowest(self):
        if not self.students: return
        worst = min(self.students, key=lambda s: self.calculate_stats(s)[1])
        self.display_output("=== LOWEST MARK ===\n\n" + self.format_student(worst))

    def sort_records(self):
        order = simpledialog.askstring("Sort", "Enter 'asc' for ascending or 'desc' for descending:")
        if order and order.lower() in ['asc', 'desc']:
            reverse = (order.lower() == 'desc')
            self.students.sort(key=lambda s: self.calculate_stats(s)[1], reverse=reverse)
            self.view_all() # Show sorted list

    def add_student(self):
        code = simpledialog.askstring("Add", "Enter Student Code (4 digits):")
        name = simpledialog.askstring("Add", "Enter Student Name:")
        # Input validation for marks
        try:
            cw1 = int(simpledialog.askstring("Add", "Coursework 1 (0-20):"))
            cw2 = int(simpledialog.askstring("Add", "Coursework 2 (0-20):"))
            cw3 = int(simpledialog.askstring("Add", "Coursework 3 (0-20):"))
            exam = int(simpledialog.askstring("Add", "Exam Mark (0-100):"))
            
            if 0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20 and 0 <= exam <= 100:
                self.students.append({'code': code, 'name': name, 'cw1': cw1, 'cw2': cw2, 'cw3': cw3, 'exam': exam})
                self.save_data()
                messagebox.showinfo("Success", "Student added.")
                self.view_all()
            else:
                messagebox.showerror("Error", "Marks out of valid range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")

    def delete_student(self):
        code = simpledialog.askstring("Delete", "Enter Student Code to delete:")
        if code:
            initial_len = len(self.students)
            self.students = [s for s in self.students if s['code'] != code]
            if len(self.students) < initial_len:
                self.save_data()
                messagebox.showinfo("Success", "Record deleted.")
                self.view_all()
            else:
                messagebox.showinfo("Not Found", "Student code not found.")

    def update_student(self):
        code = simpledialog.askstring("Update", "Enter Student Code to update:")
        student = next((s for s in self.students if s['code'] == code), None)
        
        if student:
            try:
                student['cw1'] = int(simpledialog.askstring("Update", f"New CW1 (Current: {student['cw1']}):") or student['cw1'])
                student['cw2'] = int(simpledialog.askstring("Update", f"New CW2 (Current: {student['cw2']}):") or student['cw2'])
                student['cw3'] = int(simpledialog.askstring("Update", f"New CW3 (Current: {student['cw3']}):") or student['cw3'])
                student['exam'] = int(simpledialog.askstring("Update", f"New Exam (Current: {student['exam']}):") or student['exam'])
                
                self.save_data()
                messagebox.showinfo("Success", "Record updated.")
                self.view_all()
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")
        else:
            messagebox.showinfo("Not Found", "Student code not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()