SHELL := /bin/bash

.PHONY: run
run: venv
	./venv/bin/python hanami.py

.PHONY: test
test: venv
	./venv/bin/python -m unittest discover

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	python3 -m pip install virtualenv
	python3 -m virtualenv -p python3 venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r "requirements.txt"

clean:
	rm -rf venv build __pycache__
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
