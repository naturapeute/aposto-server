deploy:
	ssh ubuntu@188.165.240.11 -p 14022 "cd ~/server && \
	git reset --hard FETCH_HEAD && \
	git pull && \
	make install && \
	make start"

start:
	source venv/bin/activate && \
	export DISPLAY=':99.0' \
	Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 & \
	uvicorn --reload --port 8080 app:app

install:
	npm install && \
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip3 install -r requirements.txt