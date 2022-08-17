# Hummingbird: A Toolkit for Distributed AWS Cloud Resource Management 

We build Hummingbird for a distributed cloud execution of Cell Profiler. We aim Hummingbird to have two major steps.

* A ParallelCluster call to start a cluster with Slurm, with images/pipelines. Our sample Cell Profiler use case has create csv method needs to be used, together with initiating with the AMI.

* Submitting the job array to Slurm.

## Install dependencies

Please use venv, rather than installing directly.

````
$ source ~/Hummingbird/bin/activate

$ pip install boto3 boto3[crt] aws-parallelcluster
````

We use [aws-parallelcluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/install-v3-after-install.html) to manage the cluster.


## Configure AWS

Install [AWS CLI](http://aws.amazon.com/cli/) and [Packer](https://www.packer.io/downloads.html).

Configure aws client locally.

````
$ aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: us-east-2
Default output format [None]:
````


Parallel Cluster proposes two approaches for a custom cluster configuration. The first approach is to [build parallel cluster AMI from our own existing base AMI](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html). Second is to modify an AWS Parallel Cluster AMI with our dependencies to build a new AMI. We use the second approach, as detailed below.

# [Modify an AWS ParallelCluster AMI](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html)

````
$ pcluster list-official-images --region us-east-2 --os ubuntu2004
{
  "images": [
    {
      "amiId": "ami-05bdb9bef9b70addd",
      "os": "ubuntu2004",
      "name": "aws-parallelcluster-3.1.4-ubuntu-2004-lts-hvm-x86_64-202205121006 2022-05-12T10-09-32.380Z",
      "version": "3.1.4",
      "architecture": "x86_64"
    },
    {
      "amiId": "ami-05e7fea4bacc5792d",
      "os": "ubuntu2004",
      "name": "aws-parallelcluster-3.1.4-ubuntu-2004-lts-hvm-arm64-202205121006 2022-05-12T10-09-44.849Z",
      "version": "3.1.4",
      "architecture": "arm64"
    }
  ]
}
````

* Create an EC2 instance with ami-05bdb9bef9b70addd above. Let's call it pcluster-hummingbird-base-big.

* Log in to this pcluster-hummingbird-base-big instance.

````
$ ssh -i "hummingbird.pem" ubuntu@ec2-18-118-25-136.us-east-2.compute.amazonaws.com  
````  
* Install [Cell-Profiler from source](https://github.com/CellProfiler/CellProfiler/wiki/Ubuntu-20.04) in the above VM.

* Run the below in the above VM.

````  
$ sudo /usr/local/sbin/ami_cleanup.sh
````

* Stop the above EC2 VM instance and create an AMI out of the instance once stopped. Let's call it pcluster-cellprofiler-hummingbird.

* Enter this image's AMI ID (ami-08ddea673d79b8450) in the [CustomAmi](https://docs.aws.amazon.com/parallelcluster/latest/ug/Scheduling-v3.html#yaml-Scheduling-SlurmQueues-Image-CustomAmi) field in the cluster configuration (cluster-config.yaml)
  
* Create a cluster.

````
$ pcluster create-cluster --cluster-configuration cluster-config.yaml --cluster-name hummingbirdcp --region us-east-2
{
  "cluster": {
    "clusterName": "hummingbirdcp",
    "cloudformationStackStatus": "CREATE_IN_PROGRESS",
    "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/cluster-name/6a621100-120d-11ed-81d4-0a23b49d510e",
    "region": "us-east-2",
    "version": "3.1.4",
    "clusterStatus": "CREATE_IN_PROGRESS"
  },
  "validationMessages": [
    {
      "level": "WARNING",
      "type": "CustomAmiTagValidator",
      "message": "The custom AMI may not have been created by pcluster. You can ignore this warning if the AMI is shared or copied from another pcluster AMI. If the AMI is indeed not created by pcluster, cluster creation will fail. If the cluster creation fails, please go to https://docs.aws.amazon.com/parallelcluster/latest/ug/troubleshooting.html#troubleshooting-stack-creation-failures for troubleshooting."
    },
    {
      "level": "WARNING",
      "type": "AmiOsCompatibleValidator",
      "message": "Could not check node AMI ami-08ddea673d79b8450 OS and cluster OS ubuntu2004 compatibility, please make sure they are compatible before cluster creation and update operations."
    }
  ]
}
````

* List clusters
````
$ pcluster list-clusters
{
  "clusters": [
    {
      "clusterName": "hummingbirdcp",
      "cloudformationStackStatus": "CREATE_IN_PROGRESS",
      "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/cluster-name/6a621100-120d-11ed-81d4-0a23b49d510e",
      "region": "us-east-2",
      "version": "3.1.4",
      "clusterStatus": "CREATE_IN_PROGRESS"
    }
  ]
}
````


* List clusters should show the current cluster to have a "CREATE_COMPLETE" status once complete.
````
$ pcluster list-clusters
{
  "clusters": [
    {
      "clusterName": "hummingbirdcp",
      "cloudformationStackStatus": "CREATE_COMPLETE",
      "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/cluster-name/6a621100-120d-11ed-81d4-0a23b49d510e",
      "region": "us-east-2",
      "version": "3.1.4",
      "clusterStatus": "CREATE_COMPLETE"
    }
  ]
}

$ pcluster describe-cluster -n hummingbirdcp
{
  "creationTime": "2022-08-09T20:48:47.075Z",
  "headNode": {
    "launchTime": "2022-08-09T20:57:29.000Z",
    "instanceId": "i-0afaa42187ed82f5a",
    "publicIpAddress": "3.145.52.0",
    "instanceType": "t2.micro",
    "state": "running",
    "privateIpAddress": "10.0.2.42"
  },
  "version": "3.1.4",
  "clusterConfiguration": {
    "url": "https://parallelcluster-344028c9583f7617-v1-do-not-delete.s3.us-east-2.amazonaws.com/parallelcluster/3.1.4/clusters/hummingbirdcp-5kt247wra9cmb3vh/configs/cluster-config.yaml?versionId=.w2tJRJz0YP5QS8kP4Q3.1JqOD38Q1G0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZBNGH7Z2TSH2LOIU%2F20220809%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20220809T210235Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8d74ad4d0f1586028f3c1a7bcb11fc3a0a96f4197f192445f6df287fc762abaf"
  },
  "tags": [
    {
      "value": "3.1.4",
      "key": "parallelcluster:version"
    }
  ],
  "cloudFormationStackStatus": "CREATE_COMPLETE",
  "clusterName": "hummingbirdcp",
  "computeFleetStatus": "RUNNING",
  "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/hummingbirdcp/a9ffb430-1824-11ed-b338-0a9410fbeefe",
  "lastUpdatedTime": "2022-08-09T20:48:47.075Z",
  "region": "us-east-2",
  "clusterStatus": "CREATE_COMPLETE"
}

$ pcluster describe-cluster-instances -n hummingbirdcp
{
  "instances": [
    {
      "launchTime": "2022-08-09T20:57:29.000Z",
      "instanceId": "i-0afaa42187ed82f5a",
      "publicIpAddress": "3.145.52.0",
      "instanceType": "t2.micro",
      "state": "running",
      "nodeType": "HeadNode",
      "privateIpAddress": "10.0.2.42"
    }
  ]

$ pcluster describe-compute-fleet -n hummingbirdcp
{
  "status": "RUNNING",
  "lastStatusUpdatedTime": ""2022-08-09T21:00:05.000Z""
}
````
