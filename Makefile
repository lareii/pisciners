PY			= python3
PIP			= pip3
VENV_PATH	= venv

$(VENV_PATH):
	$(PY) -m venv $(VENV_PATH)
	$(PIP) install -r requirements.txt

run: $(VENV_PATH)
	$(PY) main.py

clean:
	rm -rf __pycache__
	rm -rf **/__pycache__

fclean: clean
	rm -rf venv

.PHONY: run clean fclean