```
$ pcluster configure --config cluster-config.yaml
INFO: Configuration file cluster-config.yaml will be written.
Press CTRL-C to interrupt the procedure.


Allowed values for AWS Region ID:
1. ap-northeast-1
2. ap-northeast-2
3. ap-south-1
4. ap-southeast-1
5. ap-southeast-2
6. ca-central-1
7. eu-central-1
8. eu-north-1
9. eu-west-1
10. eu-west-2
11. eu-west-3
12. sa-east-1
13. us-east-1
14. us-east-2
15. us-west-1
16. us-west-2
AWS Region ID [us-east-2]:
Allowed values for EC2 Key Pair Name:
1. Kai
2. TS_DistributedCP
3. explorers
4. hummingbird
5. ssh-rsa-aws
EC2 Key Pair Name [Kai]: 4
Allowed values for Scheduler:
1. slurm
2. awsbatch
Scheduler [slurm]: 1
Allowed values for Operating System:
1. alinux2
2. centos7
3. ubuntu1804
4. ubuntu2004
Operating System [alinux2]: 4
Head node instance type [t2.micro]:
Number of queues [1]:
Name of queue 1 [queue1]:
Number of compute resources for queue1 [1]:
Compute instance type for compute resource 1 in queue1 [t2.micro]:
Maximum instance count [10]:
Automate VPC creation? (y/n) [n]: y
Allowed values for Availability Zone:
1. us-east-2a
2. us-east-2b
3. us-east-2c
Availability Zone [us-east-2a]:
Allowed values for Network Configuration:
1. Head node in a public subnet and compute fleet in a private subnet
2. Head node and compute fleet in the same public subnet
Network Configuration [Head node in a public subnet and compute fleet in a private subnet]:
Beginning VPC creation. Please do not leave the terminal until the creation is finalized
Creating CloudFormation stack...
Do not leave the terminal until the process has finished.
Stack Name: parallelclusternetworking-pubpriv-20220714152818 (id: arn:aws:cloudformation:us-east-2:621508296309:stack/parallelclusternetworking-pubpriv-20220714152818/e3d93820-0389-11ed-817b-0a5d59922b6c)
Status: Public - CREATE_COMPLETE
Status: parallelclusternetworking-pubpriv-20220714152818 - CREATE_COMPLETE
The stack has been created.
Configuration file written to cluster-config.yaml
You can edit your configuration file or simply run 'pcluster create-cluster --cluster-configuration cluster-config.yaml --cluster-name cluster-name --region us-east-2' to create your cluster.
```
