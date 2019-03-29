# hodor-server
Python REST API server with face detection and CRUD opertions. Developed for iOS App Client. 

Project created as recognizer of person opening door based on its acceleration

## Build and run

~~~~
docker build -t hodor-server .
docker run --rm --name hodor-server-container -p 8080:8080 hodor-server
docker kill hodor-server-container
~~~~
