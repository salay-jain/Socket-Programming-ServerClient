# Socket Programing: Server-Client File Sharing Protcol

In this project we have created a file sharing protocol with functionalities like
download and upload for files and indexed searching.
Following features need are implemented :
- The system should have 2 clients (acting as servers simultaneously) listening to the communication channel for requests and waiting to share files (avoiding collisions) using an application layer protocol(like FTP/HTTP).
- Each client has the ability to do the following :

	○ Know the files present on each others machines in the designated shared folders.
	
	○ Download files from this shared folder

- File transfer should incorporate MD5 checksum to handle file transfer errors.

# Commands and Intructions:

First Run ‘python3 Server.py ‘ in one terminal to start server. Then run ‘cd client then python3 Client.py ‘ in separate terminal to make and connect client to server. Then run following commands in client side to get data from server:
	
	- IndexGet shortlist <starttimestamp> <endtimestamp>  %Y-%m-%d %H:%M:%S in this format
	Output:Return ‘name’ , ‘size’ , ‘timestamp’ and ‘type’ of the files between
	the start and end time stamps to client.
	
	- BONUS​-​IndexGet shortlist <starttimestamp> <endtimestamp> *.txt or *.pdf
	Output:Return only *.txt , *.pdf files between specified time stamps to client.
	
	- history
	Output:Return all the commands ran till now from that active client

	- IndexGet longlist
	Output:Return ‘name’, ‘size’ , ‘timestamp’ and ‘type’ of all files (not
	directories) present in current working directory of server to client.
	
	- BONUS​-IndexGet longlist specific
	Output:Return longlist for only *.txt file containing word “Programmer” in it.
	
	- FileHash verify <FileName>
	Output:​ Return checksum and last modified timestamp of the input file to
	client.
	
	- FileHash checkall
	Outpu:Return filename , checksum and last modified timestamp of all the
	files in the current working directory of server.
	
	- FileDownload Path1 TCP/UDP
	Path1 - path of file to be downloaded
	Output: Download file specified in Path1 and also returns filename , filesize ,last modified timestamp and the MD5hash of the requested file.
	
	- Cache verify <Filename>
	Output:If the file is present return it from cache else “FileDownload” it and update the cache.
	
	- Cache show
	Output:Should print all elements of the cache and their sizes.
	
	- exit-Client connection closed

----------------------------------------------------------------------------------------
