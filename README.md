# Hummingbird
A Python-based toolkit for AWS Hybrid Cloud Resource Management, using Boto3

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
# Approach - 2: [Modify an AWS ParallelCluster AMI](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html)

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

* Enter this image's AMI ID (ami-08ddea673d79b8450) in the [CustomAmi](https://docs.aws.amazon.com/parallelcluster/latest/ug/Scheduling-v3.html#yaml-Scheduling-SlurmQueues-Image-CustomAmi) field in the cluster configuration and create a cluster.

# Approach - 1: Build a Custom AWS ParallelCluster AMI

* ami-09cf6eb3398323e1f is an image of Ubuntu 20.04 environment with Cell-Profiler built from source.


## [Building parallel cluster AMI from a base AMI](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html).

````
$ pcluster build-image --image-id ami-pclustercellprofiler2 --image-configuration IMAGE_CONFIG.yaml --region us-east-2

{
  "image": {
    "imageId": "ami-pclustercellprofiler",
    "imageBuildStatus": "BUILD_IN_PROGRESS",
    "cloudformationStackStatus": "CREATE_IN_PROGRESS",
    "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/ami-pclustercellprofiler/29858250-11e2-11ed-8fb7-0a59962ef124",
    "region": "us-east-2",
    "version": "3.1.4"
  }
}
````

* Describe the ongoing build progress.
````
$ pcluster describe-image --image-id ami-pclustercellprofiler2 --region us-east-2
{
  "imageConfiguration": {
    "url": "https://parallelcluster-344028c9583f7617-v1-do-not-delete.s3.us-east-2.amazonaws.com/parallelcluster/3.1.4/images/ami-pclustercellprofiler-r0ag13vfl8uoo3pl/configs/image-config.yaml?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZBNGH7Z2TSH2LOIU%2F20220801%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20220801T213917Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b5769cc5cd2293a7d876bcd54c5076c41bfbee3de4e2997dbad2e86e341a9526"
  },
  "imageId": "ami-pclustercellprofiler",
  "imageBuildStatus": "BUILD_IN_PROGRESS",
  "cloudformationStackStatus": "CREATE_IN_PROGRESS",
  "cloudformationStackArn": "arn:aws:cloudformation:us-east-2:621508296309:stack/ami-pclustercellprofiler/29858250-11e2-11ed-8fb7-0a59962ef124",
  "region": "us-east-2",
  "version": "3.1.4",
  "cloudformationStackTags": [
    {
      "value": "3.1.4",
      "key": "parallelcluster:version"
    },
    {
      "value": "ami-pclustercellprofiler",
      "key": "parallelcluster:image_name"
    },
    {
      "value": "ami-pclustercellprofiler",
      "key": "parallelcluster:image_id"
    },
    {
      "value": "parallelcluster-344028c9583f7617-v1-do-not-delete",
      "key": "parallelcluster:s3_bucket"
    },
    {
      "value": "parallelcluster/3.1.4/images/ami-pclustercellprofiler-r0ag13vfl8uoo3pl",
      "key": "parallelcluster:s3_image_dir"
    },
    {
      "value": "arn:aws:logs:us-east-2:621508296309:log-group:/aws/imagebuilder/ParallelClusterImage-ami-pclustercellprofiler",
      "key": "parallelcluster:build_log"
    },
    {
      "value": "s3://parallelcluster-344028c9583f7617-v1-do-not-delete/parallelcluster/3.1.4/images/ami-pclustercellprofiler-r0ag13vfl8uoo3pl/configs/image-config.yaml",
      "key": "parallelcluster:build_config"
    }
  ],
  "imageBuildLogsArn": "arn:aws:logs:us-east-2:621508296309:log-group:/aws/imagebuilder/ParallelClusterImage-ami-pclustercellprofiler",
  "cloudformationStackCreationTime": "2022-08-01T21:37:37.707Z"
}
````
* Pcluster to create a custom AMI.

````
$ pcluster build-image --image-id ami-emoryhummingbird --image-configuration IMAGE_CONFIG.yaml --region us-east-2
````

## Development

We aim Hummingbird to have two major steps.

Step 1 - A boto3/Python method to start a ParallelCluster with Slurm, with images/pipelines. Our sample Cell Profiler use case has create csv method needs to be used, together with initiating with the AMI.

Step 2 - Submitting the job array to Slurm.

## Running the code

### Step 1
Edit the config.py file with all the relevant information for your job. Then, start creating 
the basic AWS resources by running the following script:

 $ python3 run.py setup
 
### Step 2
After the first script runs successfully, the job can now be submitted to AWS using EITHER of the 
following commands:

 $ python3 run.py submitJob for_cmat/microgliaJob.json 
 

### Step 3
After submitting the job to the queue, we can add computing power to process all tasks in AWS. 

 $ python3 run.py startCluster for_cmat/CP_Fleet_us-east-2.json 

### Step 4
When the cluster is up and running, you can monitor progress using the following command:

 $ python3 run.py monitor files/Marklein_MicrogliaSpotFleetRequestId.json 
