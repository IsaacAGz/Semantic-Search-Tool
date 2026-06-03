VENV_BIN = venv/Scripts/python
PIP = venv/Scripts/pip

.PHONY: setup run clean

setup:
	python -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(VENV_BIN) main.py

clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +