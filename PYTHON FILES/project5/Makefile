# R-E P. Miller
# CS: Information Technology
# CSC 328_010
# Fall 2023
# Assignment #5 - Sockets (Client)
# Makefile
# Created 10/26/23 - yeah, I started a bit late if you can't tell
# Due @ 11pm 10/31/23

all: client

client:
	cp p5.py client
	chmod u+x client

clean:
	# Removes all instances of client & cleans up the dead processes in the server if there are said processes on the server Ref. - https://stackoverflow.com/questions/6381229/how-to-kill-all-processes-matching-a-name
	rm -f client *.o *~
	ps aux | grep 'rmill861' | grep './server [0-9]\{5\}' | awk '{print $$2}' | xargs -r kill -9 # -r prevents it from running when there are no relevant processes. Also outputs "stopped process" msg.

.PHONY: submit

submit:
	~schwesin/bin/submit csc328 project5
