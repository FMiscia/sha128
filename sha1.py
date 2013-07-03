#! /usr/bin/python

#Per ricavare gli argomenti
#da linea di comando
import sys
import random,string

#Conversione in esadecimale del messaggio
def convertMessage(m):
	l = range(len(m))
	for i in range(len(m)):
		l[i] = m[i].encode("hex")
		l[i] = l[i].replace("0x",'')
	return l

#Shift ciclico a 32Bit
def rotateLeft(x, n):
    return (x << n) | (x >> (32-n))

#Aggiunge i bit al messaggio secondo
#le specifiche SHA:
# 1 bit : 1
# n bit: 0  
def appendStuff(s):
	result = s
	result = result + ['80']
	while ( len(result)%64 != 56%64 ):
		result = result + ['00']
	return result

#Aggiunge la lunghezza del messaggio
def checkComplete(s):
	size = len(s)
	l = hex(size*8)[2:] 
	x = "0"*(16 - len(str(l)))
	x = x + str(l)
	t = range(8)
	t =  [x[i:i+2] for i in range(0, len(x), 2)]
	return t

#Funzione principale
def doIt(mex):
	
	#Sottoregistri SHA
	H0 = int("67452301",16)	
	H1 = int("EFCDAB89",16)
	H2 = int("98BADCFE",16)
	H3 = int("10325476",16)
	H4 = int("C3D2E1F0",16)

	blocchi = range(len(mex))

	#Spezzo il messaggio in blocchi
	#da 512 bit
	for i in range(0,len(mex)/64):
		blocchi[i] = mex[i*64:(i+1)*64]
	
	#Spezzo ogni blocco in 16 parole da 32 bit e 
	#successivamente le espando fino ad 80	
	temp = range(80)
	for j in range(len(mex)/64):
		temp = [0]*80
		x = range(4)
		i=0
		for cont in range(16):
			#Espando ogni byte a 32 bit.Notazione big-endian
			temp[cont] = int(blocchi[j][i * 4],16)<< 24
        		temp[cont] |= int(blocchi[j][i * 4 + 1],16)<< 16
        		temp[cont] |= int(blocchi[j][i * 4 + 2],16) << 8
        		temp[cont] |= int(blocchi[j][i * 4 + 3],16)
			i+=1

			#Espansione fino ad 80 parole
		for t in range (16,80):
			temp[t] = rotateLeft( (temp[t-3] ^ temp[t-8] ^ temp[t-14] ^ temp[t-16]), 1 )&0xFFFFFFFF#%4294967295
		
		a = H0
		b = H1
		c = H2
		d = H3
		e = H4

		#segue il loop centrale per il blocco corrente: eseguo 
		#una funzione che dipende dall'iterazione. Alla fine 
		#vengono ricalcolati e mischiati i valori di 
		#(a,b,c,d,e) e, finito il loop,
		#aggiornati i registri h0,h1,h2,h3,h4. 
		#Il ciclo procede poi per il blocco successivo 
		for i in range (0,80):
			if (0 <= i <= 19): 
				f = (b & c) | ((~ b) & d)
				k = int("5A827999",16)
			elif (20 <= i <= 39):
				f = b ^ c ^ d
				k = int("6ED9EBA1",16)
			elif (40 <= i <= 59):
				f = (b & c) | (b & d) | (c & d)
				k = int("8F1BBCDC",16)
			elif (60 <= i <= 79):
				f = b ^ c ^ d
				k = int("CA62C1D6",16)	
	
			buf = (rotateLeft(a,5) + f + e + k + temp[i])&0xFFFFFFFF#%4294967295

        		e = d
        		d = c
        		c = rotateLeft(b,30)
        		b = a
        		a = buf

		H0 = (H0 + a)& 0xFFFFFFFF#%4294967295
		H1 = (H1 + b)& 0xFFFFFFFF#%4294967295
		H2 = (H2 + c)& 0xFFFFFFFF#%4294967295
		H3 = (H3 + d)& 0xFFFFFFFF#%4294967295
		H4 = (H4 + e)& 0xFFFFFFFF#%4294967295

	#Digest
	digest = hex(H0)+hex(H1)+hex(H2)+hex(H3)+hex(H4)
	return digest.replace("0x",'')


def create(msg):
	msg1 = convertMessage(msg)
	msg2 = appendStuff(msg1)
	mex = msg2+checkComplete(msg)
	return doIt(mex)

def birthdayAttack(msg,c):
	t = range(len(msg))
	i=2**80
	while(i!=0):
		t = ''.join(random.sample(string.letters+string.digits+string.punctuation,len(msg)))
		#print t
		if c  == create(t):
			print msg+"---->"+c
			print t+"---->"+create(t)
			break
		i-=1

if (len(sys.argv) < 2):
	print "Usage <sha.py> <messaggio>"
else:
	msg = sys.argv[1]
	#print mex
	f = range(160)
	f = create(msg)
	print f
	#birthdayAttack(msg,f)



			
		
		

	

