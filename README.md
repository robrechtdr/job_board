## Requirements

* [Install docker](https://docs.docker.com/install/)   
* [Install docker-compose](https://docs.docker.com/compose/install/)

> Tested on docker version 20.10.7 and docker-compose version 1.29.2

## Local server (for debugging purposes)

### Setup

1. Jump into the command line of your docker-based environment.

        sudo docker-compose run web bash

      > When running **for the first time** this might take a minute or two as it ...  
      >  * downloads docker image   
      >  * does docker related setup   
      >  * installs python requirements  

2. Do Django set up from within your docker environment.

        cd job_board   
        python manage.py migrate   
        python manage.py dummy_populate    

### Running local server

        sudo docker-compose up


Now visit the api (example url) from a web client (e.g. browser):

        http://0.0.0.0:8008/api/v1/job
