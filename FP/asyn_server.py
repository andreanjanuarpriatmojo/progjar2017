import asyncore
import socket
import sys
import threading
import os

def response_list():
	listfile = os.listdir(".")
	panjang = 755
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"\nLIST DIRECTORY --> /\nDOWNLOAD --> /download:(namafile)\nUPLOAD --> /upload:(namafile)\nDELETE FILE --> /delete:(namafile)\nDELETE DIRECTORY --> /deletedirect:(namadirectory)\nMOVE FILE --> /movefile:(namafile):(tujuan)\nMOVE DIRECTORY --> /movedirect:(namadirectory):(tujuan)\nADD DIRECTORY --> /adddirect:(namadirectory)\n\n\n<-DIRECTORY->\n\n" \
		"{}". format(panjang, listfile)
	return hasil

def response_download(url):
    method, namafile = url.split(':')
    apakek = open (namafile,'r').read()
    panjang = len(apakek)
    hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: multipart/form-data\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, apakek)
    return hasil

def response_upload(url):
    method, namafile = url.split(':')
    apakek = open (namafile,'r').read()
    panjang = len(apakek)
    hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: multipart/form-data\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, apakek)
    return hasil

def response_hapus(url):
	method, namafile = url.split(':')
	apakek = os.system('rm ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"REMOVE FILE SUCCESS!"
	return hasil

def response_tambahdirect(url):
	method, namafile = url.split(':')
	apakek = os.system('mkdir ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"ADD DIRECTORY SUCCESS!"
	return hasil

	#durung isok
def response_hapusdirect(url):
	method, namafile = url.split(':')
	apakek = os.rmdir(namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 26\r\n" \
		"\r\n" \
		"REMOVE DIRECTORY SUCCESS!"
	return hasil

def response_pindahdirect(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"MOVE DIRECTORY SUCCES!"
	return hasil

def response_pindahfile(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 20\r\n" \
		"\r\n" \
		"MOVE FILE SUCCESS!"
	return hasil

class ClientHandler(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock=sock)
        self.request_message = ""
	self.reply_message=""
	return
    def handle_write(self):
	pass
    def handle_close(self):
	pass
     #fungsi melayani client
    def handle_read(self):
        data = self.recv(64)
        data = bytes.decode(data)
        self.request_message = self.request_message+data
        if (self.request_message[-4:]=="\r\n\r\n"):
            baris = self.request_message.split("\r\n")
	    baris_request = baris[0]
	    print baris_request
		
	    a,url,c = baris_request.split(" ")
	       
	    if ('/download' in url):
		  respon = response_download(url)
	    elif ('/upload' in url):
		  respon = response_upload(url)
	    elif ('/delete' in url):
		  respon = response_hapus(url)
	    elif ('/adddirect' in url):
		  respon = response_tambahdirect(url)
	    elif ('/deletedirect' in url):
		  respon = response_hapusdirect(url)
	    elif ('/movedirect' in url):
		  respon = response_pindahdirect(url)
	    elif ('/movefile' in url):
		  respon = response_pindahfile(url)
	    else:
		  respon = response_list()
            self.request_message = ""
	    self.send(respon)
	    self.close()



class WebServer(asyncore.dispatcher):
    def __init__(self, host, port):
	asyncore.dispatcher.__init__(self)
	self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	self.set_reuse_addr()
	self.bind((host, port))
	self.listen(5)
    def handle_connect(self):
	pass
    def handle_expt(self):
	self.close()
    def handle_read(self):
	pass
    def handle_write(self):
	pass
    def handle_close(self):
	pass
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            koneksi_client, alamat_client = pair
            print 'Incoming connection from %s' % repr(alamat_client)
            ClientHandler(koneksi_client)        
	    #koneksi_client.send('haha')
	    #koneksi_client.close()
	    #s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	    #s.start()

server = WebServer('localhost', 8080)
asyncore.loop()
