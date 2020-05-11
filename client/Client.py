import socket
import os
import sys
import shutil

def indexGetDisplay(skt):
	while True:
		info=skt.recv(1024).decode()
		if(info.endswith('-----')):
			print(info)
			break
		print(info)
	return

def fileHashSingle(skt):
	info=skt.recv(1024).decode()
	print(info)
	return

def fileHashMultiple(skt):
	while True:
		info=skt.recv(1024).decode()
		if(info.endswith('-----')):
			print(info)
			break
		print(info)
	return

def fileDownload(skt,filename):
	info=skt.recv(5).decode()
	if(info.endswith('-----')):
		print("File not found")
	else:
		with open(filename,'wb') as file:
			while True:
				data=skt.recv(1024)
				file.write(data)
				#print("a")		
				if(len(data)<1024):
					break
		file.close()
		print('File Downloaded')
		info=skt.recv(1024).decode()
		print(info)
	return

def fileDownloadUdp(skt,filename,udpSocket):
	info=skt.recv(5).decode()
	if(info.endswith('-----')):
		print("File not found")
		udpSocket.close()
	else:
		file=open(filename,'wb')
		data,addr=udpSocket.recvfrom(1024)
		try:	
			while(data):
				#print("A")
				file.write(data)
				udpSocket.settimeout(2)
				data,addr=udpSocket.recvfrom(1024)
		except socket.timeout:	
			file.close()
			print('File Downloaded')
			udpSocket.close()
		info=skt.recv(1024).decode()
		print(info)
	return

def cacheSizeCheck():
    fileCount=0
    size=0
    cacheSize=10064
    for root, dirs, files in os.walk("./Cache"):
    	for f in files:
    		fileCount+=1
    		fp=os.path.join(root,f)
    		#filetime=datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M:%S')
    		size+=os.stat(fp).st_size
    		#print(filetime)
    #print(size)
    #print(files)
    if(size>cacheSize):
    	files.sort(key=os.path.getmtime)
    	for file in sorted(files,key=os.path.getmtime):
    		#print(file)
    		fp=os.path.join(root,file)
    		size-=os.stat(fp).st_size
    		os.remove(fp)
    		if(size<cacheSize):
    			break
    return



def cacheVerify(skt,filename):
	presentCheck=0
	s=os.getcwd()
	d=os.getcwd()
	for root, dirs, files in os.walk("./Cache"):
		#print(root)
		#print(dirs)
		if filename in files:
			presentCheck=1
			print("Present in cache")
			info='+++++'
			skt.send(info.encode())
			s=os.path.join(root,filename)
			d=os.path.join(os.getcwd(),filename)
			shutil.copy2(s,d)
			break
	if(presentCheck==0):
		print("FileDownload it")
		info='-----'
		skt.send(info.encode())
		fileDownload(skt,filename)
		#print("a")
		s=os.path.join(os.getcwd(),filename)
		for root, dirs, files in os.walk("./Cache"):
			d=os.path.join(root,filename)
			break
		shutil.copy2(s,d)
		cacheSizeCheck()
	return

def cacheShow():
    fileCount=0
    for root, dirs, files in os.walk("./Cache"):
    	for f in files:
    		fileCount+=1
    		fp=os.path.join(root,f)
    		detail="Filename: "+f+" Size: "+str(os.stat(fp).st_size)
    		print(detail)
    
    Conclusion=str(fileCount)+" files present in Cache"
    print(Conclusion)  	
    return

c=socket.socket()
c.connect(('localhost',9999))
cmd=input("$$")
udpPort=12347
history=[]

while True:
	try:
		cmd_=cmd.strip().split(' ')
		if(cmd_[0]=='exit'):
			print("Client closed")
			c.close()
			sys.exit()
		elif(cmd_[0]=='IndexGet'):
			history.append(cmd)
			c.send(cmd.encode())
			indexGetDisplay(c)
		elif(cmd_[0]=='FileHash'):
			history.append(cmd)
			c.send(cmd.encode())
			if(cmd_[1]=='verify'):
				fileHashSingle(c)
			elif(cmd_[1]=='checkall'):
				fileHashMultiple(c)
		elif(cmd_[0]=='FileDownload'):
			history.append(cmd)
			c.send(cmd.encode())
			if(cmd_[2]=='TCP'):
				fileDownload(c,cmd_[1])
			elif(cmd_[2]=='UDP') :
				udpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				udpSocket.bind(('localhost',udpPort))
				fileDownloadUdp(c,cmd_[1],udpSocket)
		elif(cmd_[0]=='Cache'):
			history.append(cmd)
			c.send(cmd.encode())
			if(cmd_[1]=='verify'):
				cacheVerify(c,cmd_[2])
			elif(cmd_[1]=='show'):
				cacheShow()
		elif(cmd_[0]=="history"):
			for i in history:
				print(i)
		else:
			print("Invalid Command")

	except KeyboardInterrupt:
		print("Client Closed")
		c.close()
		sys.exit()
	except IndexError:
		print("Invalid Command")
		continue
	except IOError:
		print("Wrong File Path")
		continue
	cmd=input("$$")

c.close()
