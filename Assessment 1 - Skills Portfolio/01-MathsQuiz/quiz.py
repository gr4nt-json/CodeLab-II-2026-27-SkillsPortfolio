"""
Maths Quiz Application - Exercise 1
CodeLab II Programming Skills Portfolio

Acknowledgement: The boilerplate Tkinter class structure and input validation 
logic were developed with the assistance of Qwen (Generative AI). 
Prompt used: "Create a robust Tkinter class structure for a maths quiz with 
integer-only input validation."
"""

import tkinter as tk
from tkinter import messagebox
import random

class MathsQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("400x450") 
        self.root.resizable(False, False)

        # Game state variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempts = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.correct_answer = 0
        self.time_left = 15
        self.timer_id = None

        # UI Elements
        self.title_label = tk.Label(root, text="Maths Quiz", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.info_label = tk.Label(root, text="Select a difficulty level to begin.", font=("Arial", 12))
        self.info_label.pack(pady=10)

        # NEW: Timer Label
        self.timer_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="red")
        self.timer_label.pack(pady=5)

        self.problem_label = tk.Label(root, text="", font=("Arial", 24, "bold"))
        self.problem_label.pack(pady=10)

        self.answer_entry = tk.Entry(root, font=("Arial", 14), width=10, justify='center')
        # Input validation: only allow integers
        self.answer_entry.config(validate='key', validatecommand=(root.register(self.validate_input), '%P'))
        # Initially hidden
        self.answer_entry.pack_forget() 
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())

        self.submit_btn = tk.Button(root, text="Submit Answer", command=self.check_answer, state=tk.DISABLED)
        # Initially hidden
        self.submit_btn.pack_forget()

        self.display_menu()

    # --- Required Functions ---

    def display_menu(self):
        """Displays the difficulty level menu at the beginning of the quiz."""
        self.problem_label.config(text="")
        self.timer_label.config(text="")
        self.info_label.config(text="Select a difficulty level:")
        
        # Ensure entry and submit are hidden
        self.answer_entry.pack_forget()
        self.submit_btn.pack_forget()

        # Clear existing difficulty buttons if any
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                text = widget.cget('text')
                # Check for the specific button texts to remove them
                if text in ['1. Easy (Single Digit)', '2. Moderate (Double Digit)', '3. Advanced (4-Digit)']:
                    widget.destroy()

        btn_easy = tk.Button(self.root, text="1. Easy (Single Digit)", command=lambda: self.start_quiz('easy'), width=25)
        btn_easy.pack(pady=5)
        btn_mod = tk.Button(self.root, text="2. Moderate (Double Digit)", command=lambda: self.start_quiz('moderate'), width=25)
        btn_mod.pack(pady=5)
        btn_adv = tk.Button(self.root, text="3. Advanced (4-Digit)", command=lambda: self.start_quiz('advanced'), width=25)
        btn_adv.pack(pady=5)

    def random_int(self):
        """Determines the min and max values based on the chosen difficulty."""
        if self.difficulty == 'easy':
            return random.randint(1, 9)
        elif self.difficulty == 'moderate':
            return random.randint(10, 99)
        elif self.difficulty == 'advanced':
            return random.randint(1000, 9999)

    def decide_operation(self):
        """Randomly decides whether the problem is addition or subtraction."""
        return random.choice(['+', '-'])

    def display_problem(self):
        """Displays the question to the user and resets attempts."""
        self.num1 = self.random_int()
        self.num2 = self.random_int()
        self.operation = self.decide_operation()
        
        # Ensure no negative answers for subtraction
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
            
        self.correct_answer = eval(f"{self.num1} {self.operation} {self.num2}")
        self.attempts = 0
        
        self.problem_label.config(text=f"{self.num1} {self.operation} {self.num2} = ?")
        self.info_label.config(text=f"Question {self.current_question} of {self.total_questions}")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
        # NEW: Start the timer
        self.start_timer()

    def is_correct(self, user_answer):
        """Checks whether the user's answer was correct."""
        return user_answer == self.correct_answer

    def display_results(self):
        """Outputs the final score out of 100 and ranks the user."""
        self.problem_label.config(text="Quiz Finished!")
        self.answer_entry.pack_forget()
        self.submit_btn.pack_forget()
        
        # Calculate grade
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"

        msg = f"Final Score: {self.score} / 100\nGrade: {grade}\n\nWould you like to play again?"
        play_again = messagebox.askyesno("Results", msg)
        
        if play_again:
            self.display_menu()
        else:
            self.root.quit()

    # --- Helper / Logic Methods ---

    def validate_input(self, new_value):
        """Ensures the Entry widget only accepts integers or is empty."""
        if new_value == "" or new_value.lstrip('-').isdigit():
            return True
        return False

    def start_quiz(self, difficulty):
        """Initializes the quiz state and starts the first question."""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        
        # Remove menu buttons
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                text = widget.cget('text')
                if text in ['1. Easy (Single Digit)', '2. Moderate (Double Digit)', '3. Advanced (4-Digit)']:
                    widget.destroy()
                
        # Show the answer entry and submit button
        self.answer_entry.pack(pady=10)
        self.submit_btn.pack(pady=5)
        self.submit_btn.config(state=tk.NORMAL)
        
        self.next_question()

    def next_question(self):
        """Moves to the next question or ends the quiz."""
        self.current_question += 1
        if self.current_question > self.total_questions:
            self.display_results()
        else:
            self.display_problem()

    def check_answer(self):
        """Handles the logic for checking the answer and scoring."""
        user_input = self.answer_entry.get().strip()
        if not user_input: return
            
        user_answer = int(user_input)
        
        if self.is_correct(user_answer):
            self.cancel_timer() # Stop timer on correct answer
            if self.attempts == 0: self.score += 10
            elif self.attempts == 1: self.score += 5
            messagebox.showinfo("Correct!", "Well done!")
            self.next_question()
        else:
            self.attempts += 1
            if self.attempts < 2:
                messagebox.showwarning("Incorrect", "Wrong answer. You have one more try!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                self.cancel_timer()
                messagebox.showerror("Incorrect", f"Out of attempts! The correct answer was {self.correct_answer}.")
                self.next_question()

    # --- NEW: Timer Logic ---
    def start_timer(self):
        self.time_left = 15
        self.timer_label.config(text=f"Time: {self.time_left}s", fg="red")
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            # Color changes to orange when low
            if self.time_left <= 5: self.timer_label.config(fg="darkorange")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.cancel_timer()
            messagebox.showwarning("Time's Up!", "You ran out of time!")
            self.next_question()

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()