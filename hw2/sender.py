import socket
import select
import pickle
import math
import sys
from sys import getsizeof
from include import Packet

my_ip='127.0.0.1'
my_port=8000
agent_ip='127.0.0.1'
agent_port=10000
THRESHOLD=16
PAYLOAD=1024
TIMEOUT=1

class Client:
	def __init__(self):
		self.thresh = THRESHOLD
		self.window = 1
		self.not_acked = 0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((my_ip, my_port))
		self.sock.setblocking(0)
		self.sent = 0

	def file_to_packets(self, path):
		with open(path, 'rb') as f:
			data = f.read()
		size = math.ceil(len(data)/PAYLOAD)
		packets = [None]*(size+1)
		packets[0] = pickle.dumps(Packet(size+1, '', 'FIN'))
		for i in range(1,size+1):
			if i == size:
				packets[i] = pickle.dumps(Packet(i, data[(i-1)*PAYLOAD:], 'DATA'))
				break
			packets[i] = pickle.dumps(Packet(i, data[(i-1)*PAYLOAD:i*PAYLOAD], 'DATA'))
		return packets

	def start(self, path):
		all_packets = self.file_to_packets(path)
		head = 1
		while head < len(all_packets):
			self.my_send(all_packets[head:head+self.window], head)
			(fail, acked) = self.my_recv(head)
			head += self.window
			if fail == 1:
				head = acked
				self.thresh=max(self.window/2, 1)
				self.window=1
				continue
			elif fail == 3:
				head = acked
				self.thresh=max(self.window/2, 1)
				self.window=1
				print("time\tout,\t\tthreshold = %d"%self.thresh)
				continue
			elif self.window < self.thresh:	self.window *= 2
			else:							self.window += 1
		while True:
			self.my_send([all_packets[0]], 0)
			fail, acked = self.my_recv(0)
			if fail == 2:
				print("recv finack")
				self.sock.close()
				return
	
	def my_send(self, packets, head):
		for i in range(len(packets)):
			self.sock.sendto(packets[i], (agent_ip, agent_port))
			if head == 0:	print("send\tfin");	break
			if head+i <= self.sent:
				print("resnd\tdata\t\t#%d,\t"%(head+i), "winSize =", self.window)
			else:
				print("send\tdata\t\t#%d,\t"%(head+i), "winSize =", self.window)
			self.sent = max(self.sent, head+i)

	def my_recv(self, head):
		acked = head
		for i in range(self.window):
			ready = select.select([self.sock], [], [], TIMEOUT)
			if ready[0]:
				pkt, addr = self.sock.recvfrom(1200)
				pkt = pickle.loads(pkt)
				if pkt.type == 'FINACK':	return (2,0)
				print("recv\tack\t\t#%d"%pkt.seq)
				if pkt.seq != acked:		return (1,acked)
				acked += 1
			else:							return (3,acked)
		return (0,0)

if __name__ == '__main__':
	client = Client()
	client.start(sys.argv[1])
