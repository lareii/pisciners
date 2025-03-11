PY			= python3
PIP			= pip3
VENV_PATH	= venv
REQS		= requirements.txt

all: $(VENV_PATH)
	$(VENV_PATH)/bin/$(PY) main.py

$(VENV_PATH): $(REQS)
	$(PY) -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/$(PIP) install -r $(REQS)

clean:
	rm -rf __pycache__ **/__pycache__

fclean: clean
	rm -rf $(VENV_PATH)

re: fclean all

.PHONY: all clean fclean re
