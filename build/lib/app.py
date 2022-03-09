#!/usr/bin/python3
from flask import Flask, request, render_template, url_for
from settings import PORT, DEBUG
from main import Serializers, Render

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        
        bid, ask, date = Render.test()
        spread = bid - ask
        spread = '{:4f}'.format(spread)
        
        if spread > '0':
            action = 'Buy'
            
        elif spread < '0':
            action = 'Sell'
        
        else:
            action = 'Without change'
        
        return render_template('template.index.html', bid=bid, ask=ask, date=date, spread=spread, action=action)

    else:
        return render_template('template.400.html')

if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)