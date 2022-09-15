config:
	./scripts/config.sh

build-docker-etherip:
	docker-compose build etherip rf-bo rf-si

build-docker-rf: config build-docker-etherip
	docker-compose build rf-bo rf-si

build-docker-skids-rf: config
	docker-compose build p7skid p5skid linacskid

