.ONESHELL:
.PHONY: all test pydoc

all: test README.txt

test:
	python3 CommandIo.py

pydoc:
	export PYTHONDOCS=https://github.com/TakashiSasaki/command-io
	python3 -m pydoc CommandIo

README.txt: CommandIo.py
	export PYTHONDOCS=https://github.com/TakashiSasaki/command-io
	python3 -m pydoc CommandIo >$@

