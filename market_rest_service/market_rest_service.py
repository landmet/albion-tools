#!/usr/bin/env python

import argparse
from flask import Flask
from views.price_processor import prices


# Create the Flask app
app = Flask(__name__)

# Register Blueprint views
app.register_blueprint(prices, url_prefix='/prices')

# Start the Flask app if script is executed
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Albion Market API")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    if args.dev:
        app.run(host="0.0.0.0", port=8000, debug=True)
    else:
        app.run(host="0.0.0.0", port=8000, debug=True)
