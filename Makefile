server:
	python3 run.py

env:
	virtualenv env

init:
	pip install -r requirements.txt

.PHONY: server env init
