deploy:
	ssh ubuntu@188.165.240.11 -p 14022 "cd ~/server && \
	git reset --hard FETCH_HEAD && \
	git pull && \
	make install && \
	make start"

start:
	bash -c "bin/start.sh"

install:
	bash -c "bin/install.sh"
