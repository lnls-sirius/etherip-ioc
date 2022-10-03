config:
	./scripts/config.sh

build-docker-etherip:
	docker-compose build etherip

build-docker-sirius-amb-temp: config build-docker-etherip
	docker-compose build fcplc01 fcplc02 fcplc03
