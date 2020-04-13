.ONESHELL:
.PHONY: all test pydoc

all: test README.txt

test:
	python3 CommandIo.py

pydoc:
	python3 -m pydoc CommandIo

README.txt: CommandIo.py
	python3 -m pydoc CommandIo >$@

