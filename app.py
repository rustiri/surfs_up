from flask import Flask

#create a new Flask app instance
app = Flask(__name__)

#Create Flask Routes
@app.route('/')

#create function 
def hello_world():
    return 'Hello World'

