# Hummingbird: A Toolkit for Distributed AWS Cloud Resource Management 

## Build and run the container

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
sudo docker build -t hummingbird .
````

Run as nohup
````
nohup sudo docker run --name hummingbird -p 9090:8081 hummingbird > hummingbird.out &
````
