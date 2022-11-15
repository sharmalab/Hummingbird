# Hummingbird: A Toolkit for Distributed AWS Cloud Resource Management 

## Run the server container

Run as nohup
````
nohup sudo docker run --name hummingbird -p 9091:8081 -p 9090:8080 hummingbird > hummingbird.out &
````

## Run the client
````
python client.py
````

## Developer Guideline: Build the container

Clone the source code
````
git clone git@github.com:sharmalab/Hummingbird.git
````

Get the latest code
````
git pull
````

Build the container
````
sudo docker build -t hummingbird:1.0.0 .
````
Tag the container
````
docker tag hummingbird:1.0.0 pradeeban/hummingbird:1.0.0
````

Log in to Docker and push the container
````
docker login

docker push pradeeban/hummingbird:1.0.0
````
