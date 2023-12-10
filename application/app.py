from datetime import datetime
import os

from flask import Flask, render_template, request, jsonify

import events


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Return the index.html file."""
    property_id = os.getenv('GA_PROPERTY_ID')
    return render_template('index.html', property_id=property_id)

@app.route('/', methods=['POST'])
def handle_event():
    """Handle the POST request from the client-side JavaScript code."""
    response = events.handle_event(request.json, datetime.now().date().isoformat())
    app.logger.debug(f'Exchange rate: {response}')
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=True, threaded=True)
