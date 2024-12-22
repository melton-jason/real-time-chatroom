VIRTUAL_ENV ?= /usr

PYTHON = $(VIRTUAL_ENV)/bin/python
PIP = $(VIRTUAL_ENV)/bin/pip

pip_requirements:
	$(PIP) install --upgrade -r src/requirements.txt

server:
	$(PYTHON) src/server.py

client:
	$(PYTHON) src/client.py
