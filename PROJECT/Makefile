# Refer to https://stackoverflow.com/questions/6273608/how-to-pass-argument-to-makefile-from-command-line

.PHONY: all server client

all: server client

server:
	python3 server.py $(filter-out $@,$(MAKECMDGOALS))

client:
	python3 client.py $(filter-out $@,$(MAKECMDGOALS))



