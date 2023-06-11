copy_config:
	mkdir -p ~/.dock
	cp -f src/config.py ~/.dock/config.py

install:
	pip install -r requirements.txt
	pip install .

run: install
	dock