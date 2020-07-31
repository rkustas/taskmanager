from flask import Flask
from flask_cors import CORS

# print(__name__)

# Create Flask app

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)