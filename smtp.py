# -*- coding: utf-8 -*-


import socket
import ssl
import base64


from_email = '***@gmail.com'
to_email = '***@gmail.com'

msg = """
\r\nCONGRATULATIONS!!! You have been SELECTED for an EXCLUSIVE offer!!!
LIMITED TIME ONLY!!! Click here to claim your prize: http://very-suspicious-link.com/redeem-now
>>> $$$ WIN BIG $$$ <<<
ACT NOW to get INSTANT ACCESS to a wealth of amazing offers!
\n***DON'T MISS OUT ON THIS OPPORTUNITY!!!***
"""

endmsg = "\r\n.\r\n"
subject_to = "homework_email"
# 1- Choose a mail server (e.g. Google mail server) and call it mailserver
# Fill in start
mailserver = 'smtp.gmail.com'
#Fill in end

# 2- Create socket called clientSocket and establish a TCP connection with mailserver

# Fill in start
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, 587))
recv = clientSocket.recv(1024)
print(recv)
# Fill in end


# 3- Send HELLO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

cmnd = 'STARTTLS\r\n'.encode()
clientSocket.send(cmnd)
recv_cd = clientSocket.recv(1024).decode()
print(recv_cd)
if recv_cd[:3] == '220':
    clientSocket = ssl.wrap_socket(clientSocket)
else:
    print("220 reply not received from server")

def account_log(user, password):

    identification = "\x00"+user+"\x00"+password
    base64_str = base64.b64encode(identification.encode())
    register_msg = "AUTH PLAIN " + base64_str.decode()
    clientSocket.send(f"{register_msg}\r\n".encode())
    rcv_pr = clientSocket.recv(1024).decode()
    print(rcv_pr)
    if rcv_pr[:3] != '235':
        print ('235 reply not received from server.')


account_log("***@gmail.com", "fati kjlo ikkf mjbc")

# 4- Send MAIL FROM command and print server response.

# Fill in start
clientSocket.send("MAIL FROM: <from_email>\r\n".encode())
recv_2 = clientSocket.recv(1024).decode()
print(recv_2)
if recv_2[:3] != '250':
    print ('250 reply not received from server.')
# Fill in end


# 5- Send RCPT TO command and print server response.

# Fill in start
RCPT_TO = f'RCPT TO:<{to_email}>\r\n'
clientSocket.send(RCPT_TO.encode())
recv_3 = clientSocket.recv(1024).decode()
print(recv_3)
if recv_3[:3] != '250':
    print('250 reply not received from server.')
# Fill in end


# 6- Send DATA command and print server response.

# Fill in start
DATA = 'DATA\r\n'
clientSocket.send(DATA.encode())
recv_4 = clientSocket.recv(1024).decode()
print(recv_4)
if recv_4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end


# 7- Send message data.

# Fill in start
email_message = f"Subject: {subject_to}\r\n To: shayandaneshyar1379995@gmail.com \r\n{msg}"
clientSocket.send(email_message.encode())
# Fill in end


# 8- Message ends with a single period.

# Fill in start
clientSocket.send(endmsg.encode())
recv_5 = clientSocket.recv(1024).decode()
print(recv_5)
if recv_5[:3] != '250':
    print('250 reply not received from server after end of message.')
# Fill in end


# 9- Send QUIT command and get server response.

# Fill in start
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv_6 = clientSocket.recv(1024).decode()
print(recv_6)
if recv_6[:3] != '221':
    print('221 reply not received from server after QUIT command.')
# Fill in end









