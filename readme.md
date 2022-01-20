# Jetbrains Installer

A fantastic tool to install your favorite IDEs on Linux.

## Setup Development Environment

- Clone this repo: `git clone git@github.com:SindriaInc/jetbrains-installer.git`
- Move into it: `cd jetbrains-installer`
- Build local image: `bash build.sh sindriainc/jetbrains-installer local`
- Setup env: `cp .env.local .env`
- Setup docker compose: `cp docker-compose.local.yml docker-compose.yml`
- Start environment: `docker-compose up -d`
