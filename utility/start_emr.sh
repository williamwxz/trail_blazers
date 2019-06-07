#!/bin/bash

aws s3 cp preinstall.sh s3://us-immigration-data/preinstall.sh

cluster_id = `aws emr create-cluster --applications Name=Hadoop Name=Spark Name=Livy \
 --tags 'creator=Mac_CONSOLE' \
 --ec2-attributes '{"InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-8e6c7bc7","EmrManagedSlaveSecurityGroup":"sg-0af30f8cf7e97fb2b","EmrManagedMasterSecurityGroup":"sg-03b6a1630472a578d", "KeyName":"aws_rev1"}' \
 --service-role EMR_DefaultRole \
 --release-label emr-5.23.0 \
 --log-uri 's3n://aws-logs-332608265013-us-west-2/elasticmapreduce/' \
 --name 'udacity' \
 --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m3.xlarge","Name":"Master Instance Group"}]' \
 --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-west-2`

$cluster_id>>cluster_id.cfg
