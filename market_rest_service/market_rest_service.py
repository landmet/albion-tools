#!/usr/bin/env python

import argparse
from flask import Flask
from views import price_processor


# Create the Flask app
app = Flask(__name__)

# Register Blueprint views
app.register_blueprint(price_processor, url_prefix='/price')

# Start the Flask app if script is executed
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Albion Market API")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    if args.dev:
        app.run(host="0.0.0.0", port=8000, debug=True)
    else:
        app.run(host="0.0.0.0", port=8000, debug=True)
