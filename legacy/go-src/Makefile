build:
	mkdir -p target
	go build -o ./target/ai cmd/cli/main.go

backup:
	mkdir -p tmp
	go run cmd/cli/main.go openwebui backup --path tmp

setup-owui:
	go run cmd/cli/main.go openwebui setup

test:
	go test -v ./...


install-py-dev:
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt install python3.11
	# venv is essential for sanity.
	sudo apt install python3.11-venv
	# this installs libpython3.11.so
	sudo apt install python3.11-dev
