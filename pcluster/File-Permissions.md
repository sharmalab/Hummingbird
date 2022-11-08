# File permissions.

We fix folder permissions based on [FSx for Lustre guidelines](https://docs.aws.amazon.com/fsx/latest/LustreGuide/attach-s3-posix-permissions.html), as listed below in a tutorial format.

## A sample local file
First let's make a folder locally and create a file in it.

````
$ mkdir output7

$ echo "S3cp metadata import test" >> output7/s3cptest.txt

````

Let's give the new folder, public write (777) permissions.

````
$ cd ..

$ chmod -R 777 output7/
````

Let's check the permissions.
````
$ ls -ld output7/ output7/s3cptest.txt
drwxrwxrwx  3 pradeeban  staff  96 Aug 31 17:58 output7/
-rwxrwxrwx  1 pradeeban  staff  26 Aug 31 17:58 output7/s3cptest.txt
````

## Importing the file permissions to the file and the folder.

Now, how to pass on these open permissions to the file and the directory, when we upload it to an S3 bucket that is mounted to our Parallel Cluster through FSx for Lustre?

The below steps should be followed, to upload the file and folder together with the permissions, so that they will correctly reflect in the mounted directory in our Parallel Cluster node.

````
$ aws s3api put-object --bucket cmat-thrust1 --key Marklein/output7/ --metadata '{"user-agent":"aws-fsx-lustre" , "file-atime":"1595002920000000000ns", "file-owner":"ubuntu" , "file-permissions":"0100777","file-group":"ubuntu" , "file-mtime":"1595002920000000000ns"}'
{
    "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
    "VersionId": "J7OcdP8rrwyEBhrxD6SPa9iNtQlhzltJ"
}


$ aws s3api head-object --bucket cmat-thrust1 --key Marklein/output7/
{
    "AcceptRanges": "bytes",
    "LastModified": "2022-09-01T18:01:00+00:00",
    "ContentLength": 0,
    "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
    "VersionId": "J7OcdP8rrwyEBhrxD6SPa9iNtQlhzltJ",
    "ContentType": "binary/octet-stream",
    "Metadata": {
        "user-agent": "aws-fsx-lustre",
        "file-atime": "1595002920000000000ns",
        "file-owner": "ubuntu",
        "file-permissions": "0100777",
        "file-group": "ubuntu",
        "file-mtime": "1595002920000000000ns"
    }
}

$ aws s3 cp output7/s3cptest.txt s3://cmat-thrust1/Marklein/output7/s3cptest.txt --metadata '{"user-agent":"aws-fsx-lustre" , "file-atime":"1595002920000000000ns" , "file-owner":"ubuntu" , "file-permissions":"0100777","file-group":"ubuntu" , "file-mtime":"1595002920000000000ns"}'
upload: output7/s3cptest.txt to s3://cmat-thrust1/Marklein/output7/s3cptest.txt


$ aws s3api head-object --bucket cmat-thrust1 --key Marklein/output7/s3cptest.txt
{
    "AcceptRanges": "bytes",
    "LastModified": "2022-09-01T18:02:24+00:00",
    "ContentLength": 26,
    "ETag": "\"eb33f7e1f44a14a8e2f9475ae3fc45d3\"",
    "VersionId": "fPzBMEhy6skO.0367ZJ6sprFjIFo2jQ7",
    "ContentType": "text/plain",
    "Metadata": {
        "user-agent": "aws-fsx-lustre",
        "file-atime": "1595002920000000000ns",
        "file-owner": "ubuntu",
        "file-permissions": "0100777",
        "file-group": "ubuntu",
        "file-mtime": "1595002920000000000ns"
    }
}
````

## Check permissions from an EC2 instance of the Parallel Cluster
This creates a /hummingbird/Marklein/output7 directory with our s3cptest.txt file in it in the Parallel Cluster nodes. Let's check the permissions from an instance from the cluster.
````
$ cd /hummingbird/Marklein/

$ ls -ld output7/ output7/s3cptest.txt
drwxrwxrwx 2 root root 25600 Sep  1 18:17 output7/
-rwxrwxrwx 1 root root    30 Sep  1 18:17 output7/s3cptest.txt
````

These permissions are open as we wanted, and in contrast to the typical non-writeable permissions of the mounted directory.
````
$ cd ..

$ ls -ld Marklein/

drwxr-xr-x 13 root root 25600 Sep  1 18:01 Marklein/
````

