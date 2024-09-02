import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# CoinDesk API
def get_bitcoin_price():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

# News API
def get_bitcoin_news():
    response = requests.get('https://newsapi.org/v2/everything?q=bitcoin&apiKey=1f0b65cc425b48708e44f638eccaa2fb')
    data = response.json()
    
    # Check if 'articles' key exists in the response
    if 'articles' in data:
        return data['articles']
    else:
        # Handle the error or log it for further investigation
        print("Error fetching news:", data)
        return []  # Return an empty list if there's an error


# Historical Price Trends
def get_historical_prices():
    response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json')
    data = response.json()
    return data

# Quiz
def get_quiz_question():
    questions = [
        {'question': 'What is the current block reward for Bitcoin?', 'answers': ['6.25 BTC', '12.5 BTC', '25 BTC'], 'correct': 0},
        {'question': 'What is the total supply of Bitcoin?', 'answers': ['21 million', '100 million', '1 billion'], 'correct': 0},
        {'question': 'What is the name of the founder of Bitcoin?', 'answers': ['Satoshi Nakamoto', 'Vitalik Buterin', 'Nick Szabo'], 'correct': 0}
    ]
    return questions[0]

@app.route('/')
def index():
    bitcoin_price = get_bitcoin_price()
    bitcoin_news = get_bitcoin_news()
    historical_prices = get_historical_prices()
    quiz_question = get_quiz_question()
    return render_template('index.html', bitcoin_price=bitcoin_price, bitcoin_news=bitcoin_news, historical_prices=historical_prices, quiz_question=quiz_question)

@app.route('/quiz', methods=['POST'])
def quiz():
    answer = request.form['answer']
    quiz_question = get_quiz_question()
    if answer == quiz_question['answers'][quiz_question['correct']]:
        return jsonify({'result': 'correct'})
    else:
        return jsonify({'result': 'incorrect'})

@app.route('/historical_prices')
def historical_prices():
    historical_prices = get_historical_prices()
    dates = list(historical_prices.keys())
    prices = list(historical_prices.values())
    plt.plot(dates, prices)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Historical Bitcoin Prices')
    plt.show()
    return 'Historical prices graph'

if __name__ == '__main__':
    app.run(debug=True)
