import random
import tkinter as tk
import time

# Add a global variable to store the timer update task
timer_task = None
difficulty = "easy"  # Default difficulty level

# Define time limits for each difficulty level
time_limits = {
    "easy": 60,    # 60 seconds
    "medium": 45,  # 45 seconds
    "hard": 35     # 35 seconds
}

def set_difficulty(level):
    global difficulty
    difficulty = level
    difficulty_label.config(text=f"Difficulty: {level.capitalize()}")
    timer_label.config(text=f"Time: {time_limits[level]} seconds")  # Update timer label

def start_game():
    global attempts, best_score, timer, secret_number, timer_task
    attempts = 0
    timer = time_limits[difficulty]  # Set the timer based on difficulty
    secret_number = random.randint(1, 100)

    guess_entry.config(state=tk.NORMAL)
    check_button.config(state=tk.NORMAL)
    result_label.config(text="")
    message_label.config(text="")
    timer_label.config(text=f"Time: {timer} seconds")

    # Start or restart the timer
    if timer_task is not None:
        root.after_cancel(timer_task)
    update_timer()

def check_guess():
    global attempts, best_score, timer, timer_task
    attempts += 1
    guess = int(guess_entry.get())

    if guess == secret_number:
        guess_entry.config(state=tk.DISABLED)
        check_button.config(state=tk.DISABLED)
        show_congratulations_message()

        if best_score is None or attempts < best_score:
            best_score = attempts
            save_best_score(best_score)

        # Stop the timer
        if timer_task is not None:
            root.after_cancel(timer_task)
    elif guess < secret_number:
        result_label.config(text="Try a higher number.📈")
    else:
        result_label.config(text="Try a lower number.📉")

def clear_guess():
    guess_entry.delete(0, "end")

def show_congratulations_message():
    message = f"Congratulations! You guessed the correct number in {attempts} attempts."
    message_label.config(text=message, font=("Helvetica", 12, "bold"), fg="green")

def update_timer():
    global timer, timer_task
    timer -= 1
    timer_label.config(text=f"Time: {timer} seconds")
    if timer == 0:
        timer_label.config(text="Time's up!")
        guess_entry.config(state=tk.DISABLED)
        check_button.config(state=tk.DISABLED)
        result_label.config(text="Time's up! You couldn't guess the number in time.")
    else:
        timer_task = root.after(1000, update_timer)  # Store the timer task

def quit_game():
    root.quit()

def save_best_score(score):
    with open("best_score.txt", "w") as file:
        file.write(str(score))

def load_best_score():
    try:
        with open("best_score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return None

root = tk.Tk()
root.title("Guess the Number Game")
root.configure(bg="skyblue")
root.geometry("700x500")

attempts = 0
best_score = load_best_score()
secret_number = 0
timer = 0
timer_task = None

main_frame = tk.Frame(root, bg="skyblue")
main_frame.pack(pady=10)

instruction_label = tk.Label(main_frame, text="Guess the number between 1 and 100:", font=("Helvetica", 14))
instruction_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

text_frame = tk.Frame(main_frame, bg="lightblue")
text_frame.grid(row=1, column=0, columnspan=2)

guess_label = tk.Label(text_frame, text="Enter your guess:", font=("Helvetica", 12), bg="lightblue")
guess_label.grid(row=0, column=0, padx=10)

guess_entry = tk.Entry(text_frame, font=("Helvetica", 15), width=30, bd=2, state=tk.DISABLED)
guess_entry.grid(row=0, column=1, padx=10, pady=10)

buttons_frame = tk.Frame(main_frame, bg="lightblue")
buttons_frame.grid(row=2, column=0, columnspan=2)

check_button = tk.Button(buttons_frame, text="Check Guess", command=check_guess, font=("Helvetica", 12), bg="green", fg="white", state=tk.DISABLED)
check_button.grid(row=0, column=0, padx=10, pady=10)

clear_button = tk.Button(buttons_frame, text="Clear", command=clear_guess, font=("Helvetica", 12), bg="red", fg="white")
clear_button.grid(row=0, column=1, padx=10, pady=10)

quit_button = tk.Button(buttons_frame, text="Quit", command=quit_game, font=("Helvetica", 12), bg="blue", fg="white")
quit_button.grid(row=0, column=2, padx=10, pady=10)

result_label = tk.Label(main_frame, text="", font=("Helvetica", 12), bg="lightblue", fg="black")
result_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))

message_label = tk.Label(main_frame, text="", font=("Helvetica", 12, "bold"), fg="green")
message_label.grid(row=4, column=0, columnspan=2, pady=10)

best_score_label = tk.Label(root, text=f"Best Score: {best_score if best_score is not None else 'N/A'}", font=("Helvetica", 12))
best_score_label.pack(pady=5)

difficulty_frame = tk.Frame(root, bg="lightblue")
difficulty_frame.pack(pady=5)

difficulty_label = tk.Label(difficulty_frame, text="Select Difficulty:", font=("Helvetica", 12), bg="lightblue")
difficulty_label.grid(row=0, column=0, padx=10)

easy_button = tk.Button(difficulty_frame, text="Easy", command=lambda: set_difficulty("easy"), font=("Helvetica", 12), bg="lightgreen")
easy_button.grid(row=0, column=1, padx=5)

medium_button = tk.Button(difficulty_frame, text="Medium", command=lambda: set_difficulty("medium"), font=("Helvetica", 12), bg="yellow")
medium_button.grid(row=0, column=2, padx=5)

hard_button = tk.Button(difficulty_frame, text="Hard", command=lambda: set_difficulty("hard"), font=("Helvetica", 12), bg="red")
hard_button.grid(row=0, column=3, padx=5)

difficulty_label = tk.Label(difficulty_frame, text=f"Difficulty: {difficulty.capitalize()}", font=("Helvetica", 12), bg="lightblue")
difficulty_label.grid(row=1, column=0, padx=10, columnspan=4)

start_game_button = tk.Button(root, text="Start Game", command=start_game, font=("Helvetica", 12), bg="green", fg="white")
start_game_button.pack(side=tk.RIGHT, padx=10, pady=10)

timer_label = tk.Label(root, text=f"Time: {time_limits[difficulty]} seconds", font=("Helvetica", 12))
timer_label.pack(side=tk.LEFT, padx=10)

root.mainloop()
