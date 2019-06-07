#!/anaconda3/bin/python
import configparser
import boto3
import sys

CONFIG_FILE='../configurations/config.cfg'

def create_redshift(client, config):
    response = client.create_cluster(
        DBName=config.get('CLUSTER', 'DB_NAME'),
        ClusterIdentifier=config.get('CLUSTER','ClusterIdentifier'),
        ClusterType=config.get('CLUSTER', 'ClusterType'),
        NodeType=config.get('CLUSTER', 'NodeType'),
        MasterUsername=config.get('CLUSTER','DB_USER'),
        MasterUserPassword=config.get('CLUSTER', 'DB_PASSWORD'),
        VpcSecurityGroupIds=[
            config.get('CLUSTER', 'VpcSecurityGroupIds'),
        ],
        Port=int(config.get('CLUSTER', 'DB_PORT')),
        IamRoles=[
            config.get('IAM_ROLE', 'ARN'),
        ]
    )  
    return response  


def delete_redshift(client, config):
    response = client.delete_cluster(
        ClusterIdentifier=config.get('CLUSTER', 'ClusterIdentifier'),
        SkipFinalClusterSnapshot=True,
    )
    return response

def main(create=True):
    config_file = CONFIG_FILE
    config = configparser.ConfigParser()
    config.read(config_file)
    client = boto3.client('redshift', \
        region_name=config.get('AWS', 'REGION'),
        aws_access_key_id=config.get('AWS','KEY'),
        aws_secret_access_key=config.get('AWS','SECRETE'))
    if create:
        response = create_redshift(client, config)
    else:
        response = delete_redshift(client, config)
    print(response)
    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print("redshift.py create|delete")
    else:
        if sys.argv[1]=='create':
            main()
        elif sys.argv[1]=='delete':
            main(False)
        else:
            print("redshift.py create|delete")
