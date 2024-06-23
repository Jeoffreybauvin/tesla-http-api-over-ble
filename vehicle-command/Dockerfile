FROM --platform=${BUILDPLATFORM:-linux/amd64} golang:1.22 AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

RUN git clone https://github.com/teslamotors/vehicle-command.git -b v0.0.2 /usr/local/vehicle-command

WORKDIR /usr/local/vehicle-command

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
RUN go mod download && go mod verify && mkdir -p /usr/local/bin/app
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -ldflags="-w -s" -v -o /usr/local/bin/app ./...

FROM --platform=${TARGETPLATFORM:-linux/amd64} scratch

WORKDIR /usr/local/bin

COPY --from=builder /usr/local/bin/app/* /usr/local/bin/