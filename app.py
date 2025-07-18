from flask import Flask, render_template, request
from agent import run_nutrition_agent

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = ""
    meal_plan = ""
    food_input = ""

    if request.method == 'POST':
        food_input = request.form['food']
        try:
            recommendations, meal_plan = run_nutrition_agent(food_input)
        except Exception as e:
            recommendations = f"⚠️ Error: {str(e)}"
            meal_plan = "Meal plan could not be generated."

    return render_template('index.html',
                           food_input=food_input,
                           recommendations=recommendations,
                           meal_plan=meal_plan)

if __name__ == '__main__':
    app.run(debug=True)
