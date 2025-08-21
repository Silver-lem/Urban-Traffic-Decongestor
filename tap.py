#importing flask
from flask import Flask,request,jsonify
import openai
import os

#loading api key from env
openai.api_key = os.getenv("OpenAI_API_Key")

#instance of flask
app = Flask(__name__)

#Defining a route

@app.route('/')
def Hello():
    return "Hello World"

@app.route('/recommend',methods = ['POST'])
def rec():
    print()


#main driver function
if __name__ == '__main':
    app.run()