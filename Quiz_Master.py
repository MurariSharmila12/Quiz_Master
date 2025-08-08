# quiz_game.py
import csv
import random

def load_questions(filename="quiz.csv"):
    """
    Loads questions from a CSV file.
    Each row in the CSV is expected to be a dictionary.
    """
    questions = []
    try:
        # Use encoding='utf-8' to prevent character issues
        # Use newline='' to prevent blank rows
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            # DictReader reads each row as a dictionary, using the header row for keys
            reader = csv.DictReader(f)
            for row in reader:
                questions.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    
    # Validation can be added here to ensure columns exist
    if not questions or not all(k in questions[0] for k in ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']):
         print("Error: CSV file must contain the headers: question,option_a,option_b,option_c,option_d,answer")
         return None
         
    return questions

def run_quiz(questions):
    """
    Runs the main quiz loop.
    """
    random.shuffle(questions)
    
    score = 0
    total_questions = len(questions)
    
    print("--- Welcome to the CSV-Powered Python Quiz! ---")
    print(f"You will be asked {total_questions} questions. Let's begin.\n")

    for i, q_item in enumerate(questions):
        print(f"Question {i + 1} of {total_questions}: {q_item['question']}")
        
        # Display the options
        print(f"  A. {q_item['option_a']}")
        print(f"  B. {q_item['option_b']}")
        print(f"  C. {q_item['option_c']}")
        print(f"  D. {q_item['option_d']}")
        
        # Get and validate the user's answer
        while True:
            user_answer = input("Your choice (A, B, C, or D): ").upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            else:
                print("Invalid input. Please enter A, B, C, or D.")

        # Check if the answer is correct
        if user_answer == q_item['answer'].upper():
            print("Correct! Excellent.\n")
            score += 1
        else:
            correct_letter = q_item['answer'].upper()
            # Get the full text of the correct answer
            correct_text = q_item[f'option_{correct_letter.lower()}']
            print(f"Wrong! The correct answer was {correct_letter}. {correct_text}\n")
    
    # Display final results
    print("--- Quiz Over! ---")
    print(f"You answered {score} out of {total_questions} questions correctly.")
    
    percentage = (score / total_questions) * 100
    print(f"Your final score is {percentage:.2f}%")

# --- Main part of the script ---
if __name__ == "__main__":
    # 1. Load the questions from the CSV
    quiz_questions = load_questions()
    
    # 2. If questions were loaded successfully, run the quiz
    if quiz_questions:
        run_quiz(quiz_questions)