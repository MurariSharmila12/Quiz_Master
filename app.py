from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
import os

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'a_truly_secret_key_for_sessions'

# Global variable to hold all questions, loaded once on startup
QUESTIONS = []

def load_questions_on_startup():
    """Loads all questions from the CSV into the global QUESTIONS list."""
    global QUESTIONS
    questions_temp = []
    try:
        # Get the absolute path of the directory where app.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the quiz.csv file
        csv_path = os.path.join(base_dir, "quiz.csv")
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get('question'):
                    questions_temp.append(row)
        QUESTIONS = questions_temp
        print(f"--- INFO --- Successfully loaded {len(QUESTIONS)} questions on startup.")
    except FileNotFoundError:
        print(f"--- CRITICAL ERROR --- quiz.csv not found at {csv_path}. The app will not work.")
    except Exception as e:
        print(f"--- CRITICAL ERROR --- An error occurred on startup: {e}")

# Call the function here, outside the 'if __name__' block
load_questions_on_startup()

# --- ROUTES ---

@app.route('/')
def index():
    """The home page, which now asks the user to choose the number of questions."""
    total_available = len(QUESTIONS)
    return render_template('index.html', total_available=total_available)

@app.route('/start_quiz/<string:num_questions_str>')
def start_quiz(num_questions_str):
    """
    This new route sets up the quiz based on the user's choice.
    """
    total_available = len(QUESTIONS)
    
    if num_questions_str == 'all':
        num_to_ask = total_available
    else:
        num_to_ask = int(num_questions_str)

    # Make sure we don't ask for more questions than are available
    if num_to_ask > total_available:
        num_to_ask = total_available

    # Create a shuffled list of question INDICES (numbers)
    question_indices = list(range(total_available))
    random.shuffle(question_indices)
    
    # Take a slice of the desired length
    questions_for_game = question_indices[:num_to_ask]

    session['question_order'] = questions_for_game
    session['score'] = 0
    session['current_question_number'] = 0
    
    # Redirect to the first question
    return redirect(url_for('question'))

@app.route('/question')
def question():
    """Displays the current question."""
    if not QUESTIONS:
        return "<h1>Error: Questions are not loaded.</h1><p>Please check the terminal for critical errors.</p>"

    question_order = session.get('question_order', [])
    current_question_number = session.get('current_question_number', 0)

    if current_question_number >= len(question_order):
        return redirect(url_for('results'))

    question_index = question_order[current_question_number]
    q_item = QUESTIONS[question_index]
    
    return render_template('question.html', question=q_item, q_number=current_question_number + 1, total_questions=len(question_order))

@app.route('/answer', methods=['POST'])
def answer():
    """Processes the user's answer."""
    question_order = session.get('question_order', [])
    current_question_number = session.get('current_question_number', 0)
    
    user_answer_text = request.form.get('option')
    
    if current_question_number < len(question_order):
        question_index = question_order[current_question_number]
        correct_answer_text = QUESTIONS[question_index].get('answer', '')
        
        if user_answer_text == correct_answer_text:
            session['score'] = session.get('score', 0) + 1

    session['current_question_number'] = current_question_number + 1
    
    return redirect(url_for('question'))

@app.route('/results')
def results():
    """Displays the final score."""
    score = session.get('score', 0)
    total_questions = len(session.get('question_order', []))
    return render_template('results.html', score=score, total_questions=total_questions)

# This part is only for local development
if __name__ == '__main__':
    app.run(debug=True)
