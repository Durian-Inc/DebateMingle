server:
	FLASK_APP=run.py FLASK_DEBUG=1 python3 -m flask run

env:
	virtualenv env

init:
	pip install -r requirements.txt

.PHONY: server env init
