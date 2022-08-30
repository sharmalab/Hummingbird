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

* Create an Active Directory instance
````
$ aws ds describe-directories --directory-id "d-9a6718f286"
{
    "DirectoryDescriptions": [
        {
            "DirectoryId": "d-9a6718f1d9",
            "Name": "hummingbird.emory.edu",
            "ShortName": "admin",
            "Size": "Small",
            "Edition": "Standard",
            "Alias": "d-9a6718f1d9",
            "AccessUrl": "d-9a6718f1d9.awsapps.com",
            "DnsIpAddrs": [
                "172.31.6.230",
                "172.31.28.23"
            ],
            "Stage": "Active",
            "LaunchTime": "2022-08-25T17:09:23.373000-04:00",
            "StageLastUpdatedDateTime": "2022-08-25T17:38:43.078000-04:00",
            "Type": "MicrosoftAD",
            "VpcSettings": {
                "VpcId": "vpc-65323d0d",
                "SubnetIds": [
                    "subnet-b5c2f5dd",
                    "subnet-76fe930c"
                ],
                "SecurityGroupId": "sg-01d8578d38f530a14",
                "AvailabilityZones": [
                    "us-east-2a",
                    "us-east-2b"
                ]
            },
            "SsoEnabled": false,
            "DesiredNumberOfDomainControllers": 2,
            "RegionsInfo": {
                "PrimaryRegion": "us-east-2",
                "AdditionalRegions": []
            }
        }
    ]
} 
```` 
* Create a cluster.

````
$ pcluster create-cluster --cluster-configuration cluster-config.yaml --cluster-name hummingbird01 --region us-east-2
{
  "cluster": {
    "clusterName": "hummingbirdyy",
    "cloudformationStackStatus": "CREATE_IN_PROGRESS",
    "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/hummingbirdyy/b58d9090-24ce-11ed-9766-063dc7aa931a",
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
    },
    {
      "level": "WARNING",
      "type": "DomainAddrValidator",
      "message": "The use of the ldaps protocol is strongly encouraged for security reasons."
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
      "clusterName": "hummingbirdyy",
      "cloudformationStackStatus": "CREATE_COMPLETE",
      "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/hummingbirdyy/b58d9090-24ce-11ed-9766-063dc7aa931a",
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
      "clusterName": "hummingbirdyy",
      "cloudformationStackStatus": "CREATE_COMPLETE",
      "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/hummingbirdyy/b58d9090-24ce-11ed-9766-063dc7aa931a",
      "region": "us-east-2",
      "version": "3.1.4",
      "clusterStatus": "CREATE_COMPLETE"
    }
  ]
}

$ pcluster describe-cluster --cluster-name hummingbird01
{
  "creationTime": "2022-08-30T16:00:24.140Z",
  "headNode": {
    "launchTime": "2022-08-30T16:15:16.000Z",
    "instanceId": "i-02606bcdcbac61852",
    "publicIpAddress": "3.17.166.49",
    "instanceType": "t2.micro",
    "state": "running",
    "privateIpAddress": "10.0.2.189"
  },
  "version": "3.1.4",
  "clusterConfiguration": {
    "url": "https://parallelcluster-344028c9583f7617-v1-do-not-delete.s3.us-east-2.amazonaws.com/parallelcluster/3.1.4/clusters/hummingbird01-wmh0u33oht07ip87/configs/cluster-config.yaml?versionId=AdCkMs_NtWv3Ml_hd3c6laI7YHyXFNEm&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZBNGH7Z2TSH2LOIU%2F20220830%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20220830T162226Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=973c951c022d1da14653ddc4970b3522be837636450dc01db70bce8daaa14881"
  },
  "tags": [
    {
      "value": "3.1.4",
      "key": "parallelcluster:version"
    }
  ],
  "cloudFormationStackStatus": "CREATE_COMPLETE",
  "clusterName": "hummingbird01",
  "computeFleetStatus": "RUNNING",
  "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/hummingbird01/db49b550-287c-11ed-8a00-024f8cf22450",
  "lastUpdatedTime": "2022-08-30T16:00:24.140Z",
  "region": "us-east-2",
  "clusterStatus": "CREATE_COMPLETE"
}

$ pcluster describe-cluster-instances -n hummingbirdyy
{
  "instances": [
    {
      "launchTime": "2022-08-25T23:43:56.000Z",
      "instanceId": "i-0d29a454032d974b4",
      "publicIpAddress": "18.116.28.165",
      "instanceType": "t2.micro",
      "state": "running",
      "nodeType": "HeadNode",
      "privateIpAddress": "10.0.2.72"
    },
    {
      "launchTime": "2022-08-25T23:54:07.000Z",
      "instanceId": "i-0f24d66bb44cd649a",
      "queueName": "queue1",
      "instanceType": "t2.micro",
      "state": "running",
      "nodeType": "ComputeNode",
      "privateIpAddress": "10.0.52.254"
    }
  ]
}

$ pcluster describe-compute-fleet -n hummingbirdyy
{
  "status": "RUNNING",
  "lastStatusUpdatedTime": ""2022-08-09T21:00:05.000Z""
}
````

Detailed logs can be found by,
````
$ tail -f ~/.parallelcluster/pcluster-cli.log
````

* To start a worker node, issue the below command from the head node:

````
$ srun --pty bash

````

* Then, from the worker node:

````
$ cellprofiler -c -r -p /hummingbird/Marklein/Microglia_Morphology_Project/AWS_Test/Multithreading_Universal_Frozen.cppipe -i /hummingbird/Marklein/Microglia_Morphology_Project/Frozen_C20s/Plate_1/ -o /hummingbird/Marklein/Microglia_Morphology_Project/AWS_Test/Output4/Plate_1-A -d /hummingbird/Marklein/Microglia_Morphology_Project/AWS_Test/Output4/Plate_1-A/cp.is.done --data-file=/hummingbird/Marklein/Microglia_Morphology_Project/AWS_Test/images.csv -g Metadata_Plate=Plate_1,Metadata_WellRow=A

````