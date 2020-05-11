import socket
import sys
import datetime
import os
import hashlib

def shortlistFiles(c,dateInit,timeInit,dateFinal,timeFinal):
	startTime=dateInit+' '+timeInit
	endTime=dateFinal+' '+timeFinal
	files=filter(os.path.isfile,os.listdir(os.curdir))
	filesCount=0
	#print(len(files))
	for f in files:
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
		#print(filetime)
		name,ext=os.path.splitext(f)
		if(filetime>startTime and filetime<endTime):
			detail="Filename: "+f+" Size: "+str(os.path.getsize(f))+" Timestamp: "+filetime+" Extension: "+ext
			c.send(detail.encode())
			#print(detail)
			filesCount+=1
	Conclusion="Sent "+ str(filesCount)+" files details"
	print(Conclusion)
	endtag="-----"
	if(filesCount==0):
		info="No files in given timestamp"	
		c.send(info.encode())
	c.send(endtag.encode())
	print("Operarion Success")
	return

def shortlistSpeceficFiles(c,dateInit,timeInit,dateFinal,timeFinal,type):
	startTime=dateInit+' '+timeInit
	endTime=dateFinal+' '+timeFinal
	files=filter(os.path.isfile,os.listdir(os.curdir))
	filesCount=0
	#print(len(files))
	for f in files:
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
		#print(filetime)
		name,ext=os.path.splitext(f)
		if(filetime>startTime and filetime<endTime and type==ext):
			detail="Filename: "+f+" Size: "+str(os.path.getsize(f))+" Timestamp: "+filetime+" Extension: "+ext
			c.send(detail.encode())
			#print(detail)
			filesCount+=1
	Conclusion="Sent "+ str(filesCount)+" files details"
	print(Conclusion)
	endtag="-----"
	if(filesCount==0):
		info="No files in given timestamp"	
		c.send(info.encode())
	c.send(endtag.encode())
	print("Operarion Success")
	return

def longlistFiles(c):
	files=filter(os.path.isfile,os.listdir(os.curdir))
	filesCount=0
	#print(len(files))
	for f in files:
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
		#print(filetime)
		name,ext=os.path.splitext(f)
		detail="Filename: "+f+" Size: "+str(os.path.getsize(f))+" Timestamp: "+filetime+" Extension: "+ext
		c.send(detail.encode())
		print(detail)
		filesCount+=1
	
	Conclusion="Sent "+ str(filesCount)+" files details"
	print(Conclusion)
	endtag="-----"
	if(filesCount==0):
		info="No files in given Directory"	
		c.send(info.encode())
	c.send(endtag.encode())
	print("Operarion Success")
	return

def longlistSpeceficFiles(c):
	files=filter(os.path.isfile,os.listdir(os.curdir))
	filesCount=0
	#print(len(files))
	for f in files:
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
		#print(filetime)
		name,ext=os.path.splitext(f)
		if(ext=='.txt'):
			file=open(f)
			for line in file:
				line=line.strip().split()
				if "programmer" in line:
					detail="Filename: "+f+" Size: "+str(os.path.getsize(f))+" Timestamp: "+filetime+" Extension: "+ext
					c.send(detail.encode())
					#print(detail)
					filesCount+=1
					break
			file.close()

	Conclusion="Sent "+ str(filesCount)+" files details that contains word programmer"
	print(Conclusion)
	endtag="-----"
	if(filesCount==0):
		info="No files with word programmer"	
		c.send(info.encode())
	c.send(endtag.encode())
	print("Operarion Success")
	return

def fileHashSingle(c,filename):
	try:
		hashMd5=hashlib.md5()
		with open(filename,"rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hashMd5.update(chunk)
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')
		detail="Hash value : "+ hashMd5.hexdigest()+" Timestamp: "+ filetime
		print(detail)
		c.send(detail.encode())
	except:
		detail="File not found"
		c.send(detail.encode())
	print(detail)
	print("Operarion Success")
	return

def fileHashAll(c):
	files=filter(os.path.isfile,os.listdir(os.curdir))
	filesCount=0
	#print(len(files))
	for f in files:
		filesCount+=1
		hashMd5 = hashlib.md5()
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
		with open(f,"rb") as fTemp:
			for chunk in iter(lambda: fTemp.read(4096), b""):
				hashMd5.update(chunk)
		detail="Filename: "+f+" Hash value : "+ hashMd5.hexdigest()+" Timestamp: "+ filetime
		#print(detail)
		c.send(detail.encode())
	endtag="-----"
	if(filesCount==0):
		info="No files in given Directory"	
		c.send(info.encode())
	c.send(endtag.encode())
	print("Operarion Success")
	return

def fileSend(c,filename):
	try:
		file=open(filename,'rb')
		info='+++++'
		c.send(info.encode())
		packet=file.read(1024)
		while(packet):
			#print("a")
			c.send(packet)
			packet=file.read(1024)
		file.close()
		print('File sent')
		hashMd5=hashlib.md5()
		with open(filename,"rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hashMd5.update(chunk)
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')
		detail="Filename: "+filename+"  Size: " + str(os.path.getsize(filename))+" Hash value : "+ hashMd5.hexdigest()+" Timestamp: "+ filetime	
		c.send(detail.encode())
	except:
		detail="-----"
		c.send(detail.encode())
		print('Error opening file or File not found')
	return

def fileSendUdp(c,filename,udpPort,host):
	try:
		file=open(filename,'rb')
		info='+++++'
		c.send(info.encode())
		udpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		reciever=(host,udpPort)
		packet=file.read(1024)
		while(packet):
			if(udpSocket.sendto(packet,reciever)):
				#print("a")	
				packet=file.read(1024)
		file.close()
		udpSocket.close()
		print('File sent')
		hashMd5=hashlib.md5()
		with open(filename,"rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hashMd5.update(chunk)
		filetime=datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')
		detail="Filename: "+filename+"  Size: " + str(os.path.getsize(filename))+" Hash value : "+ hashMd5.hexdigest()+" Timestamp: "+ filetime	
		c.send(detail.encode())
	except:
		detail="-----"
		c.send(detail.encode())
		print('Error opening file or File not found')
	return

def cacheVerify(c,filename):
	info=c.recv(5).decode()
	if(info.endswith('+++++')):
		print("Present in cache")
	else:
		print("FileDownload it")
		fileSend(c,filename)
	return

def cacheShow():
	return

#IPV4 and TCP socket creation
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
print('Socket created')
host='localhost'
port=9999
udpPort=12347
s.bind((host,port)) 
#Can listen to 4 clients at a time
s.listen(4)   
print('Waiting for connection')
while True:
	try:
		c,addr=s.accept()
		s.settimeout(.5)
		print('Connected with',addr)

		while True:
			cmd=c.recv(1024).decode()
			cmd=cmd.strip().split(' ')
			#print(cmd)

			if(cmd[0]=='IndexGet' and cmd[1]=='shortlist'):
				if(len(cmd)==7):
					shortlistSpeceficFiles(c,cmd[2],cmd[3],cmd[4],cmd[5],cmd[6])
				elif(len(cmd)==6):
					shortlistFiles(c,cmd[2],cmd[3],cmd[4],cmd[5])
			elif(cmd[0]=='IndexGet' and cmd[1]=='longlist'):
				if(len(cmd)==3):
					longlistSpeceficFiles(c)
				elif(len(cmd)==2):
					longlistFiles(c)
			elif(cmd[0]=='FileHash'):
				if(cmd[1]=='verify'):
					fileHashSingle(c,cmd[2])
				elif(cmd[1]=='checkall'):
					fileHashAll(c)		
			elif(cmd[0]=='FileDownload'):
				if(cmd[2]=='TCP'):
					fileSend(c,cmd[1])
				elif(cmd[2]=='UDP'):
					fileSendUdp(c,cmd[1],udpPort,host)
			elif(cmd[0]=='Cache'):
				if(cmd[1]=='verify'):
					cacheVerify(c,cmd[2])
				elif(cmd[1]=='show'):
					cacheShow()
			else:
				print("Invalid Command")
				break

	except KeyboardInterrupt:
		print("Socket is closed")
		s.close()
		sys.exit()
	except socket.timeout:
		print("Client is disconnected")
		s.settimeout(None)
	c.close()

s.close()