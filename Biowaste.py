from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

# Game variables
score = 0
time_left = 60  # 1-minute timer
selected_item = random.choice(['gloves', 'syringes', 'vial', 'paper', 'cup', 'gauze', 'diaper'])
feedback_text = ""  # To store visual feedback message
game_over = False

# Game assets (file paths for waste items and bins)
waste_items = {
    'gloves': 'gloves.png',
    'syringes': 'syringes.png',
    'vial': 'vial.png',
    'paper': 'paper.png',
    'cup': 'cup.png',
    'gauze': 'gauze.png',
    'diaper': 'diaper.png'
}

bins = {
    'Yellow': 'yellowbin.jpg',
    'Red': 'redbin.jpg',
    'Translucent': 'translucentbin.png',
    'Blue': 'bluebin.png',
    'Green': 'greenbin.png'
}

item_categories = {
    'Yellow': ['gauze', 'diaper'],
    'Red': ['gloves', 'syringes'],
    'Translucent': ['syringe'],
    'Blue': ['vial'],
    'Green': ['paper', 'cup']
}

@app.route('/')
def index():
    return render_template('index.html', score=score, time_left=time_left, waste_items=waste_items, bins=bins, selected_item=selected_item, feedback=feedback_text)

@app.route('/sort/<bin_name>', methods=['POST'])
def sort_item(bin_name):
    global score, selected_item, feedback_text, game_over

    if not game_over:
        # Check if the selected waste item belongs to the bin
        if selected_item in item_categories[bin_name]:
            score += 10
            feedback_text = "Correct!"
        else:
            score -= 5
            feedback_text = "Wrong!"

        # After sorting, pick a new random item
        selected_item = random.choice(list(waste_items.keys()))

        # Send the updated data back, including the updated waste item image and score
        return jsonify({
            'score': score,
            'feedback': feedback_text,
            'selected_item': waste_items[selected_item]  # Send updated waste item image filename
        })

    return jsonify({'game_over': True, 'feedback': "Game Over! Please start a new game."})

@app.route('/update', methods=['POST'])
def update_timer():
    global time_left, score, game_over, feedback_text

    if game_over:
        return jsonify({'game_over': True, 'feedback': "Game Over! Please start a new game."})

    # Decrease time left
    time_left -= 1

    if time_left <= 0:
        game_over = True
        feedback_text = f"Game Over! Final Score: {score}"

    return jsonify({'game_over': game_over, 'time_left': time_left, 'score': score, 'feedback': feedback_text})

@app.route('/new_game', methods=['POST'])
def start_new_game():
    global score, time_left, selected_item, feedback_text, game_over

    score = 0
    time_left = 60
    selected_item = random.choice(list(waste_items.keys()))
    feedback_text = ""
    game_over = False

    return jsonify({'score': score, 'time_left': time_left, 'feedback': feedback_text, 'selected_item': waste_items[selected_item]})

if __name__ == '__main__':
    app.run(debug=True)
