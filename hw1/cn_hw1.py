import socket
import sys
import time

try:
    IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'irc.freenode.net'
port = 6667
botnick = 'b04902105_bot'
remote_ip = socket.gethostbyname(host)

f = open('config', 'r')
chan = f.readline().split('=')[1].strip('"')
chan = chan[1:-2]

IRCSocket.connect((remote_ip, port))
print('socket connected to ' + host + ' on ip ' + remote_ip)

IRCSocket.sendall(("User " + botnick + " " + botnick + " " + botnick + " :This is a bot!\n").encode('utf-8'))
IRCSocket.sendall(("Nick " + botnick + "\n").encode('utf-8'))
message = "JOIN " + chan + "\r\n"
IRCSocket.sendall(message.encode('utf-8'))
IRCSocket.sendall(('/nick ' + botnick).encode('utf-8'))

while True:
    recv_msg = IRCSocket.recv(4096).decode("UTF-8")
    print('receive: ', recv_msg)
    if recv_msg.find('JOIN') != -1:
        IRCSocket.send(bytes('PRIVMSG ' + chan + ' : Hi! I\'m a robot\r\n', 'utf-8'))
    if recv_msg.find('PING') != -1:
        IRCSocket.send(bytes('PONG ' + recv_msg.split(':')[1] + '\r\n', 'utf-8'))
    if recv_msg.find('killbot') != -1:
        IRCSocket.send(bytes('PRIVMSG ' + chan + " : " + "Oh shit I'm dead!\r\n", "utf-8"))
        break
    if recv_msg.find('@repeat ') != -1:
        msg = recv_msg.split('@repeat ')[1]
        IRCSocket.send(bytes('PRIVMSG ' + chan + ' : ' + msg + '\r\n', "UTF-8"))
    if recv_msg.find('@convert ') != -1:
        msg = recv_msg.split('@convert ')[1].strip()
        if msg[:2] == '0x':
            try:
                IRCSocket.send(bytes('PRIVMSG ' + chan + ' : ' + str(int(msg, 0)) + '\r\n', "UTF-8"))
            except ValueError:
                IRCSocket.send(bytes('PRIVMSG ' + chan + ' : WRONG FORMAT\r\n', "UTF-8"))
        else:
            try:
                IRCSocket.sendall(bytes('PRIVMSG ' + chan + " : " + str(hex(int(msg))) + '\r\n', "UTF-8"))
            except ValueError:
                IRCSocket.send(bytes('PRIVMSG ' + chan + ' : WRONG FORMAT\r\n', "UTF-8"))
    if recv_msg.find('@ip ') != -1:
        ip = recv_msg.split('@ip ')[1].strip()
        L = len(ip)
        try:
            float(ip)
        except ValueError:
                IRCSocket.send(bytes('PRIVMSG ' + chan + ' : WRONG FORMAG\r\n', "UTF-8"))
                continue
        ans = [[]]
        for i in range(1, L):
            for j in range(i, L):
                for k in range(j, L):
                    if i <= 3 and j-i <= 3 and k-j <=3 and L-k <= 3:
                        if i == j or j == k or k == L:  continue
                        #if float(ip[0]) == 0:  continue
                        if i > 1 and float(ip[0]) == 0:    continue
                        if j-i > 1 and float(ip[i]) == 0:    continue
                        if k-j > 1 and float(ip[j]) == 0:    continue
                        if len(ip)-k > 1 and float(ip[k]) == 0: continue
                        if (float(ip[:i]) < 256) and (float(ip[i:j]) < 256) and (float(ip[j:k]) < 256) and (float(ip[k:]) < 256):
                            ans.append([i, j, k])
        s = ""
        IRCSocket.send(bytes('PRIVMSG ' + chan + ' : ' + str(len(ans)-1) + '\r\n', "UTF-8"))
        for i in ans[1:]:
            tmp = str(ip)
            for k in range(L):
                if k in i:
                    s = s + '.'
                s = s + tmp[k]
            IRCSocket.sendall(bytes('PRIVMSG ' + chan + " : " + s + '\r\n', "UTF-8"))
            s = ""
            time.sleep(1)
    if recv_msg.find('@help') != -1:
        IRCSocket.send(bytes('PRIVMSG ' + chan + ' : @repeat <Message>\r\n', "UTF-8"))
        IRCSocket.sendall(bytes('PRIVMSG ' + chan + " : @convert <Number>\r\n", "UTF-8"))
        IRCSocket.sendall(bytes('PRIVMSG ' + chan + " : @ip <String>\r\n", 'UTF-8'))

