# Deploy Immutables Azure

This IaC component permit parallel deployment of immutable resources on azure cloud.

This is atomic routine for any CI/CD such as gitlab-ci, bitbucket-pipelines etc.
In any case is possible to use it manually with run.sh helper script.


## Setup Development Environment

- Clone this repo: `git clone git@github.com:SindriaInc/jetbrains-installer.git`
- Move into it: `cd jetbrains-installer`
- Build local image: `bash build.sh sindriainc/jetbrains-installer local`
- Setup env: `cp .env.local .env`
- Setup docker compose: `cp docker-compose.local.yml docker-compose.yml`
- Start environment: `docker-compose up -d`