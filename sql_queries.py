import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('configurations/config.cfg')

KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')
REGION                 = config.get('AWS', 'REGION')

DB_NAME        = config.get('CLUSTER', 'DB_NAME')
DB_USER        = config.get('CLUSTER', 'DB_USER')
DB_PASSWORD            = config.get('CLUSTER', 'DB_PASSWORD')
DB_PORT                = config.get('CLUSTER', 'DB_PORT')

IAM_ROLE      = config.get("IAM_ROLE", "ARN")

DEMOGRAPHICS_DATA = config.get('S3', 'DEMOGRAPHICS_DATA')
IMMIGRATION_DATA = config.get('S3', 'IMMIGRATION_DATA')
IMMIGRATION_DATA = config.get('S3', 'AIRPORT_DATA')

DEMOGRAPHICS_TABLE="demographics"
IMMIGRATION_TABLE="immigration"
AIRPORT_TABLE="airport"

BUCKET='s3://'+config.get('S3', 'BUCKET')+'/'

# Schema
CREATE_DEMOGRAPHICS_TABLE="""
Create Table If Not Exists {}(
    city varchar,
    state varchar,
    median_age float,
    male_population int,
    femail_population int,
    population int,
    num_of_veterans int,
    foreign_born int,
    avg_household_size float,
    state_code varchar,
    race varchar,
    count int,
)
""".format(DEMOGRAPHICS_TABLE)

# redshift query
COPY_DEMOGRAPHICS_DATA_FROM_S3="""
copy {}
from {}
iam_role {}
region {}
format as csv
delimiter as ';';
""".format(DEMOGRAPHICS_TABLE, BUCKET+DEMOGRAPHICS_DATA, IAM_ROLE, REGION)

COPY_INFORMATION_DATA_FROM_S3="""
copy {}
from {}
iam_role {}
region {}
format as csv
delimiter as ',';
""".format(IMMIGRATION_TABLE, BUCKET+IMMIGRATION_DATA, IAM_ROLE, REGION)

COPY_AIRPORT_DATA_FROM_S3="""
copy {}
from {}
iam_role {}
region {}
format as csv
delimiter as ',';
""".format(AIRPORT_TABLE, BUCKET+IMMIGRATION_DATA, IAM_ROLE, REGION)


