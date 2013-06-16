import hashlib
from pyDes import *

def encrypt2(pw, key):
	data = pw 
	k = triple_des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	d = k.encrypt(data)
	print "Encrypted: %r" % d
	print "Decrypted: %r" % k.decrypt(d)
	assert k.decrypt(d, padmode=PAD_PKCS5) == data
	return d
'''	
m = hashlib.md5()
m.update("My password in a sentence")
print m.digest()
'''

data = "To be encrypted"
k = triple_des("1234567812345678", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
d = k.encrypt(data)
print "Encrypted: %r" % d
print "Decrypted: %r" % k.decrypt(d)
assert k.decrypt(d, padmode=PAD_PKCS5) == data


epw = encrypt2('password', '1234567812345678')

print epw
	
	
	
	"""
	def encrypt(pw, key):
	pwList = list(pw)
	keyList = list(key)
	pwListInt = convertToInt(pwList)
	keyListInt = convertToInt(keyList)
	
	
	
	print pwListInt
	print keyListInt
	encryptedPw = ""
	for i in pwListInt:
		encryptedPw += str(i) + '-'
	return encryptedPw
	
	def decrypt(pw, key=''):
	splitPW = pw.split('-')
	del splitPW[-1]
	pw = ""
	for i in splitPW:
		if i != '':
			pw += chr(int(i))
	return pw

def convertToInt(theList):
	intList = []
	for i in range(len(theList)):
		intList.append(ord(theList[i]))
		
	return intList


	"""


	
