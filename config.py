# Constants (User configurable)

APP_NAME = 'Marklein_Microglia'                # Used to generate derivative names unique to the application.

# DOCKER REGISTRY INFORMATION:
DOCKERHUB_TAG = 'cellprofiler/distributed-cellprofiler:2.0.0_4.1.3'

# AWS GENERAL SETTINGS:
AWS_REGION = 'us-east-2'
AWS_PROFILE = 'default'                 # The same profile used by your AWS CLI installation
SSH_KEY_NAME = 'hummingbird.pem'      # Expected to be in ~/.ssh
AWS_BUCKET = 'cmat-thrust1'

# EC2 AND ECS INFORMATION:
ECS_CLUSTER = 'default'
CLUSTER_MACHINES = 4
MACHINE_TYPE = ['r6i.xlarge']     # this has 8GB per core, 4 cores.
machine_cores = 4       # cores - please look up on AWS website based on machine type
machine_mem = 32        # in GB - please look up on AWS website based on machine type
docker_max_mem = 14     # container MAX mem in GB. default microglia pipeline uses about 12GB. This is the limiting factor.
counts_by_mem = machine_mem // docker_max_mem
# prefer 1 core per container.
TASKS_PER_MACHINE = min(machine_cores, counts_by_mem)

MACHINE_PRICE = 0.10
EBS_VOL_SIZE = 30                       # In GB.  Minimum allowed is 22.
DOWNLOAD_FILES = 'False'

# DOCKER INSTANCE RUNNING ENVIRONMENT:
DOCKER_CORES = machine_cores // TASKS_PER_MACHINE    # Number of CellProfiler processes to run inside a docker container
CPU_SHARES = DOCKER_CORES * 1024        # ECS computing units assigned to each docker container (1024 units = 1 core)
MEMORY = docker_max_mem * 1000
SECONDS_TO_START = 30                 # Wait before the next CP process is initiated to avoid memory collisions

# LOG GROUP INFORMATION:
LOG_GROUP_NAME = APP_NAME

# REDUNDANCY CHECKS
CHECK_IF_DONE_BOOL = 'True'  #True or False- should it check if there are a certain number of non-empty files and delete the job if yes?
EXPECTED_NUMBER_FILES = 5    #What is the number of files that trigger skipping a job?
MIN_FILE_SIZE_BYTES = 1      #What is the minimal number of bytes an object should be to "count"?
NECESSARY_STRING = 'csv'        #Is there any string that should be in the file name to "count"?

# PLUGINS
USE_PLUGINS = 'False'
