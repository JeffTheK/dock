copy_config:
	mkdir -p ~/.dock
	cp -f src/config.py ~/.dock/config.py

run:
	python3 src/main.py