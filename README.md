# Hummingbird: A Toolkit for Distributed AWS Cloud Resource Management 

## Developer Guidelines: Build the container

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

## Deployment Guidelines: Deploying to AWS Fargate

Define an AWS policy (hummingbirds3):
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
````

The AmazonECSTaskExecutionRolePolicy is pre-defined as below:
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
````

Define the task:

Follow the task_definition.json in defining the task.


Create a cluster as a service, using the defined task.


## User Guidelines: Run the client

Replace the urls to be the public urls of the deployed fargate service in client.py.

Run the client.py.

````
python client.py
````