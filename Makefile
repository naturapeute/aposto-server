deploy:
	ssh ubuntu@188.165.240.11 -p 14022 "cd ~/server && \
	git reset --hard FETCH_HEAD && \
	git pull && \
	sudo ln -s aposto-server.service /etc/systemd/system/ ; \
	sudo systemctl daemon-reload && \
	sudo systemctl restart aposto-server"

start:
	bash -c "bin/start.sh"

install:
	bash -c "bin/install.sh"
