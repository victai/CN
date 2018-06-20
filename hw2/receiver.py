import socket
import pickle
import sys
from include import Packet

my_ip='127.0.0.1'
my_port=9000
agent_ip='127.0.0.1'
agent_port=10000
BUFFER_SIZE=32

class Server:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((my_ip, my_port))
		self.sock.settimeout(None)
		self.buf = [None]*(BUFFER_SIZE+1)

	def flush(self, length, path):
		with open(path, 'ab') as f:
			for i in range(1,length+1):
				f.write(self.buf[i])
		self.buf = [None]*(BUFFER_SIZE+1)
		print("flush")

	def start(self, path):
		received = 0
		buf_idx = 0
		while True:
			pkt, addr = self.sock.recvfrom(1200)
			pkt = pickle.loads(pkt)
			if pkt.seq == received+1 and pkt.type == 'FIN':
				print("recv\tfin")
				ack_pkt = pickle.dumps(Packet(1, '', 'FINACK'))
				self.sock.sendto(ack_pkt, (agent_ip, agent_port))
				print("send\tfinack")
				self.flush(buf_idx, path)
				break
			if pkt.seq == received+1:
				if buf_idx == BUFFER_SIZE:
					print("drop\tdata\t#%d"%pkt.seq)
					self.flush(BUFFER_SIZE, path)
					buf_idx = 0
					ack_pkt = pickle.dumps(Packet(received, '', 'ACK'))
					self.sock.sendto(ack_pkt, (agent_ip, agent_port))
					print("send\tack\t#%d"%received)
				else:
					print("recv\tdata\t#%d"%pkt.seq)
					received += 1
					buf_idx += 1
					self.buf[buf_idx] = pkt.msg
					ack_pkt = pickle.dumps(Packet(received, '', 'ACK'))
					self.sock.sendto(ack_pkt, (agent_ip, agent_port))
					print("send\tack\t#%d"%received)
			else:
				print("drop\tdata\t#%d"%pkt.seq)
				ack_pkt = pickle.dumps(Packet(received, '', 'ACK'))
				self.sock.sendto(ack_pkt, (agent_ip, agent_port))
				print("send\tack\t#%d"%received)

			
		self.sock.close()

if __name__ == '__main__':
	server = Server()
	server.start(sys.argv[1])
