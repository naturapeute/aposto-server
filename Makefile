deploy:
	ssh aposto "cd ~/server && \
	git reset --hard FETCH_HEAD && \
	git pull && \
	sudo ln -s ~/server/aposto-server.service /etc/systemd/system/ ; \
	sudo systemctl daemon-reload && \
	make install && \
	sudo systemctl restart aposto-server"

start:
	bash -c "bin/start.sh"

install:
	bash -c "bin/install.sh"

dev:
	bash -c "bin/dev.sh"

test:
	python -m unittest -v
