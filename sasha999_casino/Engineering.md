# Engineering Document (Generally for use by SANS or Challenge enginnering)


### Version: `0.1.0`
### Long Title: Casino
### Short Title: PWN01

## Hosting:

- Host the zip file containing `casino.c`, `casino`, `build_docker.sh`, `Dockerfile` as a download on RIO
- Host the service (the provided docker container) on port 1337

## Delivery:

- Player downloads the zip file from RIO to craft their exploit on their system.
- Player connects to service and attempts exploit

## Dependancies: 

- Online storage
- Docker and a public IP