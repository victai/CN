class Packet:
	def __init__(self, seq, msg, msgtype):
		self.seq = seq
		self.msg = msg
		self.type = msgtype
