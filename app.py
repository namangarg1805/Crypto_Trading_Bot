from flask import Flask, render_template, request
from CoinSwitch_trading import all_coins
app = Flask(__name__)
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    my_list = all_coins().json()["data"]["coinswitchx"]
    strategies = ["dipshit","second"]
    selected_value = None  # Initialize selected_value

    if request.method == 'POST':
        selected_value = request.form.get("my_list")

    return render_template('index.html', my_strategy = strategies,my_list=my_list, selected_value=selected_value)

def mylist:
    return select

if __name__ == '__main__':
    app.run(debug=True)
