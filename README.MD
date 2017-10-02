# hodor-server

## Build and run

~~~~
docker build -t hodor-server .
docker run --rm --name hodor-server-container -p 8080:8080 hodor-server
docker kill hodor-server-container
~~~~