# LAM 4 DOC
Initiative for Modeling the Legal Analysis Methodology (LAM): Document generation service

# Installation

Make sure that you are running `Docker` and have the correct permissions set. If not, run the following lines to install it. 

```bash
sudo apt -y install docker.io docker-compose

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

To build 
```bash
make build-services
```
and run the containers:
```bash
make start-services
```

Install test/dev dependencies:

```bash
make install-dev
```

To run the tests:
> Make sure you have the python dependencies installed and your virtual environment activated (if you're using one).
```bash
make test
```

# Usage

## Start services
To run the docker containers for the `lam` `api` and `ui`:

```bash
make start-services
```

The LAM services are split into:

service | URL | info
------- | ------- | ----
`lam-api` | [localhost:5000](http://localhost:5000) | _access [localhost:5000/ui](http://localhost:5000/ui) for the swagger interface_ 
`lam-ui` | [localhost:9000](http://localhost:9000) |

## Stop services
To stop the containers run:
```bash
make stop-services
```

# Contributing
You are more than welcome to help expand and mature this project. We adhere to [Apache code of conduct](https://www.apache.org/foundation/policies/conduct), please follow it in all your interactions on the project.   

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the maintainers of this repository before making a change.

## Licence 
This project is licensed under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) licence. 

Powered by [Meaningfy](https://github.com/meaningfy-ws).