# Hummingbird
A Python-based toolkit for AWS Hybrid Cloud Resource Management, using Boto3

## Install dependencies
````
$ pip install boto3 boto3[crt] aws-parallelcluster
````

We use [aws-parallelcluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/install-v3-after-install.html) to manage the cluster.


## Configure AWS

Install [AWS CLI](http://aws.amazon.com/cli/).

Configure aws client locally.

````
$ aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: us-east-2
Default output format [None]:
````

Use pcluster client to manage the cluster in the specified region.

````
$ pcluster list-clusters
````


## Development

We aim Hummingbird to have two major steps.

Step 1 - A boto3/Python method to start a ParallelCluster with Slurm, with images/pipelines. Our sample Cell Profiler use case has create csv method needs to be used, together with initiating with the AMI.

Step 2 - Submitting the job array to Slurm.
