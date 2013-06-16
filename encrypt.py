import hashlib
from pyDes import *





def encrypt2(pw, key, mode=1):
	data = pw 
	k = triple_des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	if mode==1:
		d = k.encrypt(data)
		print "Encrypted: %r" % d
		return d
	elif mode==2:
		j = k.decrypt(pw)
		#assert k.decrypt(pw, padmode=PAD_PKCS5) == data
		return j

def decrypt2(pw, key):
	print 'decrypt2 key len: ', len(key)
	k = triple_des('1234567812345678', CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	return k.decrypt(pw, padmode=PAD_PKCS5)
	
def main():
	epw = encrypt2('password', '1234567812345678',1)
	print epw
	print encrypt2(epw, '1234567812345678',2)
	
if __name__=="__main__": main()
	
