# Quiz Game.py - Stable Version (No Timer)

import csv
import random
import time
import os

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_questions(filename="quiz.csv"):
    """
    Loads questions from a CSV file.
    This version is updated to safely handle blank rows in the CSV.
    """
    questions = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if the row is not empty and has a 'question' value.
                if row and row.get('question'):
                    processed_row = {
                        key: value.strip() if isinstance(value, str) else ""
                        for key, value in row.items()
                    }
                    questions.append(processed_row)
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

def ask_question(q_item):
    """
    Asks a single question and gets the user's answer.
    This is a simplified version without the timer.
    """
    print(f"{q_item['question']}")
    print(f"  A. {q_item['option_a']}")
    print(f"  B. {q_item['option_b']}")
    print(f"  C. {q_item['option_c']}")
    print(f"  D. {q_item['option_d']}")

    # Loop until the user provides a valid answer (A, B, C, or D)
    while True:
        user_answer = input("\nYour choice (A, B, C, or D): ").upper().strip()
        if user_answer in ['A', 'B', 'C', 'D']:
            return user_answer
        else:
            print("Invalid input. Please enter A, B, C, or D.")


def run_quiz(questions, num_questions_to_ask):
    """Runs the main quiz loop."""
    score = 0
    questions_to_ask = questions[:num_questions_to_ask]
    
    print("\n--- Let's Begin The Quiz! ---")
    time.sleep(2)

    for i, q_item in enumerate(questions_to_ask):
        clear_screen()
        print(f"--- Question {i + 1} of {len(questions_to_ask)} ---")
        print(f"Current Score: {score}/{i}")
        
        user_answer_letter = ask_question(q_item)

        correct_answer_text = q_item['answer']
        is_correct = False

        # Get the text of the option the user selected
        chosen_option_key = f'option_{user_answer_letter.lower()}'
        chosen_option_text = q_item.get(chosen_option_key, "")
        
        # Compare the text of the chosen option with the correct answer's text
        if chosen_option_text == correct_answer_text:
            is_correct = True
        
        if is_correct:
            print("\nCorrect! Excellent.")
            score += 1
        else:
            # Find the letter of the correct answer to display it
            correct_letter = ''
            for letter in ['a', 'b', 'c', 'd']:
                if q_item.get(f'option_{letter}') == correct_answer_text:
                    correct_letter = letter.upper()
                    break
            print(f"\nWrong! The correct answer was {correct_letter}. {correct_answer_text}")

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