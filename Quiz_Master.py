# Quiz Game.py - Upgraded Version

import csv
import random
import time
import threading

# This list will be used to get the answer from our input thread
answer_container = []

def load_questions(filename="quiz.csv"):
    """Loads questions from a CSV file."""
    questions = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                questions.append(row)
    except FileNotFoundError:
        print(f"--- ERROR! ---")
        print(f"The file '{filename}' was not found.")
        print("Please make sure your CSV file is in the same folder and named correctly.")
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
        # The timing symbol '⏳' and carriage return '\r' create a nice one-line countdown
        timer_symbol = '⏳'
        print(f"{timer_symbol} Time left: {t:02d}s ", end='\r')
        time.sleep(1)
        if not input_thread.is_alive():
            # User has answered, so we can stop the countdown
            break
    
    print() # Move to the next line after the countdown/answer

    if input_thread.is_alive():
        # The 15 seconds are up, but the input thread is still waiting.
        print("--- Time's up! ---")
        return None # Return None to indicate a timeout
    else:
        # User answered in time.
        user_answer = answer_container[0]
        if user_answer in ['A', 'B', 'C', 'D']:
            return user_answer
        else:
            # User answered, but with invalid input
            print("Invalid input given.")
            return "INVALID"


def run_quiz(questions, num_questions_to_ask):
    """Runs the main quiz loop with the selected number of questions."""
    score = 0
    
    # We only ask the number of questions the user chose
    questions_to_ask = questions[:num_questions_to_ask]
    
    print("\n--- Let's Begin The Quiz! ---")

    for i, q_item in enumerate(questions_to_ask):
        print(f"\n--- Question {i + 1} of {len(questions_to_ask)} ---")
        
        user_answer = ask_question_with_timer(q_item, 15) # 15-second time limit

        if user_answer is None: # Timeout
            pass # The timeout message is already printed
        elif user_answer == q_item['answer'].upper():
            print("Correct! Excellent.")
            score += 1
        else: # Covers wrong answers and invalid answers
            correct_letter = q_item['answer'].upper()
            correct_text = q_item[f'option_{correct_letter.lower()}']
            print(f"Wrong! The correct answer was {correct_letter}. {correct_text}")
    
    print("\n--- Quiz Over! ---")
    print(f"You answered {score} out of {len(questions_to_ask)} questions correctly.")
    
    if len(questions_to_ask) > 0:
        percentage = (score / len(questions_to_ask)) * 100
        print(f"Your final score is {percentage:.2f}%")

# --- Main part of the script that runs first ---
if __name__ == "__main__":
    all_questions = load_questions()
    
    if all_questions:
        random.shuffle(all_questions) # Shuffle all questions once at the start
        total_available = len(all_questions)

        print("--- Welcome to the Ultimate Quiz Game! ---")
        
        while True: # Loop until user gives a valid choice
            print(f"\nYou can choose to answer 10, 15, or all ({total_available}) questions.")
            choice = input("How many questions would you like to answer? (10/15/all): ").lower().strip()
            
            if choice == '10' and total_available >= 10:
                num_to_ask = 10
                break
            elif choice == '15' and total_available >= 15:
                num_to_ask = 15
                break
            elif choice == 'all':
                num_to_ask = total_available
                break
            else:
                print("Invalid choice or not enough questions available. Please try again.")

        run_quiz(all_questions, num_to_ask)
