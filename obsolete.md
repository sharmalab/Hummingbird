This is a summary of how the [Distributed CellProfiler](https://github.com/tcpan/Distributed-CellProfiler) runs. This does not reflect Hummingbird, and as such is obsolete. However, this documents the approach we took before in the Distributed Cell Profiler.

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
