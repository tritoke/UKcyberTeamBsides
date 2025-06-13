# Engineering Document (Generally for use by SANS or Challenge enginnering)


### Version: `0.1.a`
### Long Title: my challenge
### Short Title: FOR01

## Hosting:

Hosted as a flat file in an S3 bucket, Azure Storage or in RIO as a download
or
An API service running on a Ubuntu VM, with port 8080 exposed. 

## Delivery:

Player downloads flat file
or
Player connects to service and attempts exploit

## Dependancies: 

Online storage
or
Apache, subdomin name querable from the public internet, public IP