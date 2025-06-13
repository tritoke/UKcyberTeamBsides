#!/bin/bash
sudo docker build -t pwn_casino .
sudo docker run -p1337:1337 -it pwn_casino