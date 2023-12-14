all: server client

server:
	cp server.py server
	chmod u+x server

client:
	cp client.py client
	chmod u+x client
	
.PHONY: clean
	
clean:
	rm -rf client
	rm -rf server
