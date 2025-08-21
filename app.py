#importing flask
from flask import Flask
from openai import OpenAI

client = OpenAI()



#instance of flask
app = Flask(__name__)

#Defining a route

@app.route('/')
def home():
    return "Traffic AI Backend is Running 🚦"

@app.route('/rec',methods = ['POST'])
def hello():
    return "some"



#main driver function
if __name__ == '__main':
    app.run(debug = "True")