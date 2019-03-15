htmlResponse = """
HTTP/1.1 200 OK
Connection: Closed
Date: Mon, 25 Nov 15:51:56 NST
Server: Apache/2.2.14 (Win32)
Last-Modified: Mon, 25 Nov 15:51:56 NST
"""

htmlLength = """Content-Length: """

htmlType = """
Content-Type: text/html

"""

txtResponse = """
HTTP/1.1 200 OK
Connection: Closed
Date: Mon, 25 Nov 15:51:56 NST
Server: Apache/2.2.14 (Win32)
Last-Modified: Mon, 25 Nov 15:51:56 NST
Content-Length: 37
Content-Type: text/plain

"""
jpgResponse = """
HTTP/1.1 200 OK
Connection: Closed
Date: Mon, 25 Nov 15:51:56 NST
Server: Apache/2.2.14 (Win32)
Last-Modified: Mon, 25 Nov 15:51:56 NST
Content-Length: 7000
Content-Type: image/jpeg

"""

errorResponse = """
HTTP/1.1 404 OK
Connection: Closed
Date: Mon, 25 Nov 15:51:56 NST
Server: Apache/2.2.14 (Win32)
Last-Modified: Mon, 25 Nov 15:51:56 NST
Content-Length: 120
Content-Type: text/html

"""

def addQuestion(newQuestion):
	words = newQuestion.split("+")
	newQuestion = ""
	for word in words:
		if (word.find("%") == -1):
			newQuestion = newQuestion + word + " "
		else:
			newQuestion = newQuestion + word[:word.find("%")] + "?"
	print(newQuestion)
	f = open("list.html", "r")
	contents = f.readlines()
	f.close()

	contents.insert(9, "  <li>" + newQuestion + "</li>\n")
	print(contents)
	f = open("list.html", "w")
	contents = "".join(contents)
	f.write(contents)
	f.close()

from socket import *
import os

port = 80
socket = socket(AF_INET, SOCK_STREAM)
socket.bind(('', port)) 
socket.listen(10)
while True:
	conSocket, addr = socket.accept()
	data = str(conSocket.recv(1024))
	print(data)
	data = data[data.find("/") + 1:]
	questionIndex = data.find("question")
	if questionIndex != -1:
		newQuestion = data[questionIndex + 9:]
		print(newQuestion)
		addQuestion(newQuestion)
	data = data[:data.find(" ")]
	print(data)
	if data == "":
		try:
			file = open("index.html", "rb")
		except FileNotFoundError:
			file = open("error.html", "rb")
	else:
		try:
			file = open(data, "rb")
		except :
			file = open("error.html", "rb")
	response = ""
	if data == "index.html" or data == "" or data == "list.html":
		size = os.stat(file.name).st_size
		response = htmlResponse + htmlLength + str(size) + htmlType
	elif data == "index.txt":
		response = txtResponse
	elif data == "favicon.jpg" or data == "favicon.ico":
		response = jpgResponse
	else:
		response = errorResponse
	conSocket.send(response.encode("utf-8"))
	try:
		conSocket.send(file.read())
	except ConnectionAbortedError:
		continue
	conSocket.close()