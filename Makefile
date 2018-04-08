server:
	FLASK_APP=run.py FLASK_DEBUG=1 python3 -m flask run

prod:
	FLASK_APP=run.py flask run --host=0.0.0.0 --port=80

env:
	virtualenv env

init:
	pip install -r requirements.txt

.PHONY: server env init
