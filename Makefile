ORG = maestro
NAME = neural-net-builder
SHA1 = $(shell git log -1 --pretty=oneline | cut -c-10)
BRANCH = $(shell git branch -a --contains $(SHA1) | egrep '(remotes/|\*)' | egrep -v "(HEAD|detached)" | head -1 | sed -e "s/\* //" -e "s/.*\///")
VERSION = $(BRANCH)-$(SHA1)
REGISTRY = docker-registry.ticket-tool.com:5000
PORT = 4242

all: build

build:
	docker build --rm -t $(ORG)/$(NAME):${VERSION} .

	docker tag $(ORG)/$(NAME):${VERSION} $(ORG)/$(NAME):$(BRANCH)-latest

push:
	docker tag $(ORG)/$(NAME):${VERSION} $(REGISTRY)/$(ORG)/$(NAME):${VERSION}
	docker tag $(ORG)/$(NAME):${VERSION} $(REGISTRY)/$(ORG)/$(NAME):$(BRANCH)-latest
	docker push $(REGISTRY)/$(ORG)/$(NAME)

clean:
	docker kill $(NAME); docker rm $(NAME)

run:
	docker run \
		--name $(NAME) \
		-p 6006:6006 \
		-p 80:8080 \
		-v ${CURDIR}/modelBackups:/app/modelBackups \
		-e TZ="Europe/Paris" \
		-d $(ORG)/$(NAME):${VERSION}

tensorboard:
	docker exec \
		-d $(NAME) \
		tensorboard --logdir=tensorboardLogs

flush:
	rm -rf modelBackups

test:
	cd unitTests && pwd && npm test

go:
	docker exec \
		-ti $(NAME) \
		bash
