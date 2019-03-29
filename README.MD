# hodor-server
Python REST API server with face detection and CRUD opertions. Developed for iOS App Client. 

Project created as recognizer of a person opening the doors based on acceleration. Project closed, not finished.

## Build and run

~~~~
docker build -t hodor-server .
docker run --rm --name hodor-server-container -p 8080:8080 hodor-server
docker kill hodor-server-container
~~~~
