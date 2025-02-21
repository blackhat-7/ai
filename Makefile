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
