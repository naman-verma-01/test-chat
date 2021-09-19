from flask import Flask, render_template, make_response, redirect, request, session
from flask_socketio import SocketIO, send, emit
import os
from flask_session import Session

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


	
@app.route("/")
def index():
	if not session.get("name"):
		return redirect("/login")
	
	return render_template('index.html')

	
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session["name"] = request.form.get("name")
		return redirect("/")
	return render_template("login.html")
	
	
@socketio.on("message")
def handleMessage(data):
    emit("new_message",session.get("name") + " : " + data,broadcast=True)
    
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5004)
