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

Choose region N. Virginia (us-east-1) at Amazon Elastic Container Service (ECS).

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


Define the cluster:

Create a cluster as a service, using the defined task.

Choose "Capacity Provider Strategy"

Use "Fargate" as the capacity provider.

Platform Version: Latest

Deployment Configuration: Service

Task Definition: hummingbird (defined above), Revision, latest.

Service name: Any string

Service type: Replica

Desired Tasks: 1

Deployment options: Leave the default values (Rolling update)

Deployment failure detection  
Use the Amazon ECS deployment circuit breaker? Yes

Rollback on failures? Yes

Turn on Service Connect.

Choose "Client and Server"

Choose a namespace (hummingbird)

Add port mappings and applications (hummingbird-80-tcp, hummingbird, hummingbird, 80)

Use log collection (Amazon Cloud Watch)

Networking: Choose the default VPC

Create a new security group.
Security group name: hummingbird
Description: allow80

Turn on Public IP.

Allow "HTTP" (port 80) traffic from anywhere for inbound traffic.

Load balancer: Application Load Balancer.

Create a new load balancer.

Load balancer name: hummingbird

container to load balance: (choose hummingbird 80:80)

Listener: (Choose "Create new listener")
Port: 80
Target group name: hummingbird
Everyone else left default

Service autoscaling: (Select "Use service autoscaling")

Minimum number of tasks: 1
Maximum number of tasks: 3

Choose Target Tracking

Policy Name: hummingbird

ECS service metric: ECSServiceAverageMemoryUtilization

Target Value: 70

Scale-out cooldown period: 300

Scale-in cooldown period: 300

Tags are optional and can be ignored.

Start the service. Once it successfully, started, confirm that by going to the public IP address from your browser.

The public IP address can be found from the cluster > service > Task.

The public IP address should show the hummingbird home page.

## User Guidelines: Run the client

Replace the urls to be the public urls of the deployed fargate service in client.py.

Run the client.py.

````
python client.py
````

To test the server container separately (instead of going through the steps above to deploy it on ECS), you can run it locally or on a server, stand-alone. 

````
nohup sudo docker run --name hummingbird -p 80:80 pradeeban/hummingbird:1.0.3 > hummingbird.out &
````
Then change the url of the client to point to this server url, and rerun the client.py as above.
