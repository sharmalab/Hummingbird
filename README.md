# Hummingbird
A Python-based toolkit for AWS Hybrid Cloud Resource Management, using Boto3

## Install dependencies
````
$ pip install boto3 boto3[crt] aws-parallelcluster
````

We use [aws-parallelcluster](https://aws-parallelcluster.readthedocs.io/en/latest/getting_started.html) to manage the cluster.


## Configure AWS

Install [AWS CLI](http://aws.amazon.com/cli/).

Configure aws client locally.

````
$ aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: us-east-1
Default output format [None]:
````
