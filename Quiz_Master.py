# Quiz Game.py - Corrected Version

import csv
import random
import time
import threading
import os

# This list will be used to get the answer from our input thread
answer_container = []

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_questions(filename="quiz.csv"):
    """Loads questions from a CSV file."""
    questions = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Strip whitespace from all values to prevent matching errors
                # Add a check to ensure the value is a string before stripping
                cleaned_row = {}
                for key, value in row.items():
                    if isinstance(value, str):
                        cleaned_row[key] = value.strip()
                    else:
                        cleaned_row[key] = value # Keep non-string values as they are
                questions.append(cleaned_row)
    except FileNotFoundError:
        print(f"--- ERROR! ---")
        print(f"The file '{filename}' was not found.")
        print("Please make sure your CSV file is in the same folder and named correctly.")
        return None
    except Exception as e:
        print(f"--- ERROR! ---")
        print(f"An error occurred while reading the file: {e}")
        return None
    return questions

def get_user_input():
    """Target function for the input thread to get user answer."""
    user_answer = input("Your choice (A, B, C, or D): ").upper()
    answer_container.append(user_answer)

def ask_question_with_timer(q_item, time_limit):
    """Asks a single question with a timer and visual countdown."""
    global answer_container
    answer_container = []  # Clear the container for each new question

    print(f"{q_item['question']}")
    print(f"  A. {q_item['option_a']}")
    print(f"  B. {q_item['option_b']}")
    print(f"  C. {q_item['option_c']}")
    print(f"  D. {q_item['option_d']}")

    # Start the thread that waits for user input
    input_thread = threading.Thread(target=get_user_input)
    input_thread.daemon = True  # Allows main program to exit even if thread is running
    input_thread.start()

    # Main thread runs the countdown
    for t in range(time_limit, -1, -1):
        timer_symbol = '⏳'
        print(f"{timer_symbol} Time left: {t:02d}s ", end='\r')
        time.sleep(1)
        if not input_thread.is_alive():
            # User has answered, so we can stop the countdown
            break

    print() # Move to the next line after the countdown/answer

    if input_thread.is_alive():
        print("--- Time's up! ---")
        return None # Return None to indicate a timeout
    else:
        user_answer = answer_container[0]
        if user_answer in ['A', 'B', 'C', 'D']:
            return user_answer
        else:
            print("Invalid input given.")
            return "INVALID"

def run_quiz(questions, num_questions_to_ask):
    """Runs the main quiz loop with the selected number of questions."""
    score = 0
    questions_to_ask = questions[:num_questions_to_ask]

    print("\n--- Let's Begin The Quiz! ---")
    time.sleep(2)

    for i, q_item in enumerate(questions_to_ask):
        clear_screen()
        print(f"--- Question {i + 1} of {len(questions_to_ask)} ---")
        print(f"Current Score: {score}/{i}")

        user_answer_letter = ask_question_with_timer(q_item, 15) # 15-second time limit

        # The correct answer's full text is stored in q_item['answer']
        correct_answer_text = q_item['answer']
        is_correct = False

        # Check if the user's answer is correct
        if user_answer_letter and user_answer_letter != "INVALID":
            # Get the text of the option the user selected (e.g., text from 'option_c')
            chosen_option_key = f'option_{user_answer_letter.lower()}'
            chosen_option_text = q_item[chosen_option_key]

            # Compare the text of the chosen option with the correct answer's text
            if chosen_option_text == correct_answer_text:
                is_correct = True

        # Display the result
        if is_correct:
            print("\nCorrect! Excellent.")
            score += 1
        else:
            # This block now handles ALL non-correct cases: wrong, invalid, and timeout.
            # We must find the letter of the correct answer to display it.
            correct_letter = ''
            for letter in ['a', 'b', 'c', 'd']:
                option_key = f'option_{letter}'
                if q_item[option_key] == correct_answer_text:
                    correct_letter = letter.upper()
                    break

            # Print the final feedback for the question
            if correct_letter:
                print(f"\nWrong! The correct answer was {correct_letter}. {correct_answer_text}")
            else:
                # This is a fallback in case the answer in the CSV doesn't match any of the options
                print(f"\nWrong! The correct answer was: {correct_answer_text}")

        time.sleep(3) # Pause to let the user read the feedback

    clear_screen()
    print("--- Quiz Over! ---")
    print(f"You answered {score} out of {len(questions_to_ask)} questions correctly.")

    if len(questions_to_ask) > 0:
        percentage = (score / len(questions_to_ask)) * 100
        print(f"Your final score is {percentage:.2f}%")

# --- Main part of the script that runs first ---
if __name__ == "__main__":
    all_questions = load_questions("quiz.csv")

    if all_questions:
        random.shuffle(all_questions)
        total_available = len(all_questions)

        print("--- Welcome to the Ultimate Quiz Game! ---")

        while True:
            print(f"\nYou can choose to answer 10, 15, or all ({total_available}) questions.")
            choice = input("How many questions would you like to answer? (10/15/all): ").lower().strip()

            try:
                if choice == 'all':
                    num_to_ask = total_available
                    break
                elif int(choice) in [10, 15]:
                    if total_available >= int(choice):
                        num_to_ask = int(choice)
                        break
                    else:
                        print(f"Not enough questions available for your choice. Max is {total_available}.")
                else:
                    print("Invalid choice. Please enter 10, 15, or 'all'.")
            except ValueError:
                print("Invalid input. Please enter a number (10, 15) or the word 'all'.")

        run_quiz(all_questions, num_to_ask)