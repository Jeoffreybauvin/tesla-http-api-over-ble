# tesla-http-api-over-ble
Use my custom HTTP API as a proxy for making BLE requests to your Tesla

For now, it supports only ONE Tesla's VIN by API. 

# What this repository does

My goal here is to get back access to the Tesla API. And I don't want to play with the new Fleet API. 

So, I started using the [vehicle-command](https://github.com/teslamotors/vehicle-command) provided by Tesla and more precisely the BLE command `tesla-control`.

Once the BLE access to my Tesla was ok, I developed a homemade API to launch a docker container with the `tesla-control` command.

I'm providing two Docker images :

- The first is the tesla vehicle-command SDK. See below for building it (part Tesla Vehicle-Command SDK), or use [my builded image on Docker Hub](https://hub.docker.com/r/jeoffrey54/tesla-vehicle-command).
- The second, is a light image with Docker and my homemade API. See below for building it (part Build the API image), or use [my builded image on Docker Hub](https://hub.docker.com/r/jeoffrey54/tesla-http-api-over-ble)

The available commands of the BLE `tesla-control` is here : https://github.com/Jeoffreybauvin/tesla-http-api-over-ble/blob/master/settings.py#L10

# BLE access to your Tesla

> [!IMPORTANT]
> BLE means Bluetooth Low Energy : you'll need a Bluetooth dongle and the Tesla near it in order to use this project.

This guide is tested with a Tesla Model 3 2022, mine ;).

## Build and launch the API image

```
make build
```

If you want to run it, let's check the docker-compose.yml file in the repo. 

There are 3 useful environment variables :

- `VIN`: The Tesla's VIN of your vehicle
- `PRIVATE_KEY_FILE`: The path of your generated private key
- `DOCKER_IMAGE_TESLA_VEHICLE_COMMAND`: The name of the builded tesla-vehicle-command. By default, it's the one from Docker Hub.

> [!IMPORTANT]
> By default, the API runs ot the port 8000. The Swagger documentation is exposed on this path : `/docs`


## Tesla Vehicle-Command SDK

I'm providing a custom Docker image for the Tesla [vehicle-command](https://github.com/teslamotors/vehicle-command). Let's build it. Clone this repo, and launch :

```
cd vehicle-command ; make build
```

And then, test it :

```
docker run -ti tesla-vehicle-command:latest /usr/local/bin/tesla-control -h
```

If you're able to see the help of the tesla-control's command, let's continue.

## Pairing with your Tesla

First, let's generate a private key :

```
openssl ecparam -genkey -name my_custom_name -noout > private.pem
```

Then, generate the public key :

```
openssl ec -in private.pem -pubout > public.pem
```

Next, let's launch the previously builded image. Don't forget to use a volume where the generated keys are stored :

```
docker run --net=host --privileged --rm -ti -v /home/bob/tesla:/tesla tesla-vehicle-command:latest bash
```

- `--net-host` and `--privileged` are mandatory in order to use the Bluetooth key of your server/PC/whatever.
- `/home/bob/tesla` is the directory where we previously generated the public and private key.

Once connected to the container, let's try to pair with our Tesla :

```
./tesla-control -vin {VIN} -ble add-key-request {path_to_the_public_key_along_with_the_public_key_file_name} {ROLE} {FORM_FACTOR}
```

- `{VIN}` is the  Vehicle Identification Number.
- `{path_to_the_public_key_along_with_the_public_key_file_name}` should be `/tesla/public.pem`
- `{ROLE}` is one of : `owner` or `driver`
- `{FORM_FACTOR}` is one of `nfc_card`, `ios_device`, `android_device`, `cloud_key`. On my side, I used "cloud_key".

Once issued, this command should return with the following response :

```
Sent add-key request to VIN. Confirm by tapping NFC card on center console.
```

In your vehicle, use your NFC card on the center console, and a message will appear on the car display screen. 

Once validated, you should receive a notification on your phone. It should be ok.

You can now test with a new command :

```
./tesla-control -ble -vin {VIN} -key-name {path_to_the_public_key_along_with_the_public_key_file_name} -key-file {path_to_the_public_key_along_with_the_public_key_file_name} unlock
```

`unlock` should unlock your car ;).

# Todolist

- [x] Last Python version
- [ ] Support multiple VINs
- [ ] Better handling of errors
- [ ] Feel free to ask ;)