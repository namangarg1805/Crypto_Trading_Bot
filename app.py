from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    my_list = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    strategies = ["dipshit","second"]
    selected_value = None  # Initialize selected_value

    if request.method == 'POST':
        selected_value = request.form.get("my_list")

    return render_template('index.html', my_strategy = strategies,my_list=my_list, selected_value=selected_value)

if __name__ == '__main__':
    app.run(debug=True)
