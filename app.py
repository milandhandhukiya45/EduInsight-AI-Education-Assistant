from flask import Flask, render_template, request
from agent import run_education_agent  # ✅ change function import

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = ""
    learning_plan = ""
    education_input = ""  # ✅ renamed from food_input

    if request.method == 'POST':
        education_input = request.form['education']  # ✅ renamed form input
        try:
            recommendations, learning_plan = run_education_agent(education_input)  # ✅ call correct agent
        except Exception as e:
            recommendations = f"⚠️ Error: {str(e)}"
            learning_plan = "Learning plan could not be generated."

    return render_template('index.html',
                           education_input=education_input,  # ✅ update template variables
                           recommendations=recommendations,
                           learning_plan=learning_plan)

if __name__ == '__main__':
    app.run(debug=True)

