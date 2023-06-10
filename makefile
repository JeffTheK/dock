copy_config:
	mkdir -p ~/.dock
	cp -f src/config.py ~/.dock/config.py

build:
	python3 setup.py sdist

install: build
	pip install -r requirements.txt
	pip install .

run: install
	dock