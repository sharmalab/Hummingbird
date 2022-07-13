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