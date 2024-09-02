import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Configuration
COINDESK_API_URL = 'https://api.coindesk.com/v1/bpi'
NEWS_API_URL = 'https://newsapi.org/v2/everything'
NEWS_API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

# CoinDesk API
def get_bitcoin_price():
    response = requests.get(f'{COINDESK_API_URL}/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

# News API
def get_bitcoin_news():
    params = {
        'q': 'bitcoin',
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()
    return data['articles']

# Historical Price Trends
def get_historical_prices():
    response = requests.get(f'{COINDESK_API_URL}/historical/close.json')
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
    plt.savefig('historical_prices.png')  # Save the plot to a file
    return 'Historical prices graph'

if __name__ == '__main__':
    app.run(debug=True)