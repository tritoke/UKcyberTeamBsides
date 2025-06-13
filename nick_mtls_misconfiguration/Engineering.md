# Engineering Document (Generally for use by SANS or Challenge enginnering)


### Version: `1.0.0`
### Long Title: Mutually Assured Security
### Short Title: TBC

## Hosting:

Start the Docker containers using Docker Compose (or other method)

Preferably, use URLs for the different services, and set the following environment variables in Source/.env before building.

TLS certs must be passed through to the Nginx - other services can have TLS terminated at a CDN/similar.

## Delivery:

User connects directly to the running web servers.

## Dependencies: 

Some way of running containers
