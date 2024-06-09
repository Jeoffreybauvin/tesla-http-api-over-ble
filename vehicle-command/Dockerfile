FROM golang:1.22

RUN git clone https://github.com/teslamotors/vehicle-command.git -b v0.0.2 /usr/local/vehicle-command

WORKDIR /usr/local/vehicle-command

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
RUN go mod download && go mod verify && mkdir -p /usr/local/bin/app ; go build -v -o /usr/local/bin/app ./...

WORKDIR /usr/local/bin/app

CMD ["/bin/bash"]