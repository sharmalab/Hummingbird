# Hummingbird: A Toolkit for Distributed AWS Cloud Resource Management 

## Run the server container

Run as nohup
````
nohup sudo docker run --name hummingbird -p 80:80 hummingbird:1.0.3 > hummingbird.out &
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
sudo docker build -t hummingbird:1.0.3 .
````
Tag the container
````
docker tag hummingbird:1.0.3 pradeeban/hummingbird:1.0.3
````

Log in to Docker and push the container
````
docker login

docker push pradeeban/hummingbird:1.0.3
````

Config files in
````
/opt/slurm-files
````