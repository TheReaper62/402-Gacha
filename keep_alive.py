from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  string = "<body>\
              <style>\
                body {background-color: powderblue;}\
                h1,p   {text-align: center;}\
                p      {font-weight: bold;}\
              </style>\
              <h1>Bot Status</h1>\
              <hr>\
              <p>402 Gacha Online</p>\
              Version Alpha Build 1.0.1\
            </body>"
  return string

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()