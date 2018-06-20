import socket
import pickle
from random import random

my_ip='127.0.0.1'
my_port=10000
sender_ip='127.0.0.1'
sender_port=8000
receiver_ip='127.0.0.1'
receiver_port=9000

class Agent:
	def __init__(self):
		self.ip = my_ip
		self.port = my_port
		self.loss_cnt = 0
		self.pkt_cnt = 0
		self.loss_rate = 0.0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((my_ip, my_port))
	
	def drop(self):
		self.pkt_cnt += 1
		if random() < 0.1:
			self.loss_cnt += 1
			self.loss_rate = float(self.loss_cnt)/self.pkt_cnt
			return 1
		self.loss_rate = float(self.loss_cnt)/self.pkt_cnt
		return 0

	def listen(self):
		while True:
			message, addr = self.sock.recvfrom(1200)
			pkt = pickle.loads(message)
			if pkt.type == 'ACK':
				print("get\tack\t#%d"%pkt.seq) 
				print("fwd\tack\t#%d"%pkt.seq) 
				pkt = pickle.dumps(pkt)
				self.sock.sendto(pkt, (sender_ip, sender_port))
			elif pkt.type == 'DATA':
				print("get\tdata\t#%d"%pkt.seq)
				if self.drop():	print("drop\tdata\t#%d,\tloss rate = %f"%(pkt.seq, self.loss_rate));continue
				else:			print("fwd\tdata\t#%d,\tloss rate = %f"%(pkt.seq, self.loss_rate))
				pkt = pickle.dumps(pkt)
				self.sock.sendto(pkt, (receiver_ip, receiver_port))
			elif pkt.type == 'FIN':
				print("get\tfin")
				print("fwd\tfin")
				pkt = pickle.dumps(pkt)
				self.sock.sendto(pkt, (receiver_ip, receiver_port))
			elif pkt.type == 'FINACK':
				print("get\tfinack")
				print("fwd\tfinack")
				pkt = pickle.dumps(pkt)
				self.sock.sendto(pkt, (sender_ip, sender_port))
				return

if __name__ == '__main__':
	agent = Agent()
	agent.listen()
