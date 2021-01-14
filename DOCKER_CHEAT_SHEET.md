# Docker Cheet Sheet

Usefull commands:

#### Display versions

- `docker -v`
- `docker-compose -v`

#### Delete image

- `docker rm image [IMAGE IDs]`

### Run a command in a new container

- `docker run -it python:3.6 bash` starts container with image python3.6 [FETCHS IT IF NON EXISTENT] interactibly and runs bash command.

### Docker - Compose

- `sudo docker-compose run --rm [SERVICE] [COMMAND]` to run a particular service with commands and then remove image
- `sudo docker-compose down -v` remove images, networks and volumes. (--remove-orphans)
- `sudo docker-compose run --entrypoint bash bianca_web` avoid entrypoint and enter bash inside container

### Debugging a running container

- `docker container ls` to see all containers
- `docker run -it [CONTAINER ID] bash` to inspect container. Generally to list all files with ls and to watch processes with ps -aux.
- Host of each service is the name of the service, so running a service called web you can ping web from it or other services or containers and by default should get a response.
- Connect to docker container via IP (use case ex verify db connectivity): `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id` 


#### Common issues:

- Forgetting to expose port
- Trying to connect to DB in localhost:5432 [link](https://stackoverflow.com/a/45638423). Connect to postgres:5432 instead.
- Specify correctly directory/context folder in the docker-compose.yml [link](https://stackoverflow.com/a/53946016)
- whoami? Root? Nooooo. 

### Postgres:

- [Docs](https://hub.docker.com/_/postgres)
- Used image in this project [link](https://github.com/docker-library/postgres/blob/03e769531fff4c97cb755e4a608b24935ceeee27/11/Dockerfile)
- Ensure table creation: `docker-compose exec [DB SERVICE] psql --username=[USERNAME] --dbname=[DB NAME]` then `\l`
- Ensure volume creation: `docker volume inspect [NAME OF PROJECT]_[VOLUME NAME]`

#### Common issues:

- Port 5432 already in use if we let docker choose the host port automatically wWhen checking if we can accept connections to lets say 0.0.0.0:5432 it will map probably to local postgres. Map the db to another port (say 1200) and check connections there.
- invalid mount path: 'pgdata=/var/lib/postgresql/data' mount path must be absolute -> ../var

### Network between containers

- `docker network create [NET NAME]`
- `docker network ls` list all networks

#### Network connect

- [Docs](https://docs.docker.com/engine/reference/commandline/network_connect/)
- `docker network connect --alias db --alias mysql multi-host-network container2`
