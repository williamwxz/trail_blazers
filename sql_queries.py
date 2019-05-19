import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('configurations/config.cfg')

KEY                    = config.get('AWS','KEY')
SECRETE                 = config.get('AWS','SECRETE')
REGION                 = config.get('AWS', 'REGION')

DB_NAME        = config.get('CLUSTER', 'DB_NAME')
DB_USER        = config.get('CLUSTER', 'DB_USER')
DB_PASSWORD            = config.get('CLUSTER', 'DB_PASSWORD')
DB_PORT                = config.get('CLUSTER', 'DB_PORT')

IAM_ROLE      = config.get("IAM_ROLE", "ARN")

DEMOGRAPHICS_DATA = config.get('S3', 'DEMOGRAPHICS_DATA')
IMMIGRATION_DATA = config.get('S3', 'IMMIGRATION_DATA')
AIRPORT_DATA = config.get('S3', 'AIRPORT_DATA')

DEMOGRAPHICS_TABLE="demographics"
IMMIGRATION_TABLE="immigration"
AIRPORT_TABLE="airport"
TABLES=[DEMOGRAPHICS_TABLE, IMMIGRATION_TABLE, AIRPORT_TABLE]

BUCKET='s3://'+config.get('S3', 'BUCKET')+'/'

# Schema
CREATE_DEMOGRAPHICS_TABLE="""
Create Table If Not Exists {}(
    city                 varchar,
    state                varchar,
    median_age           float,
    male_population      int,
    femail_population int,
    population int,
    num_of_veterans int,
    foreign_born int,
    avg_household_size float,
    state_code varchar,
    race varchar,
    count int
)
""".format(DEMOGRAPHICS_TABLE)

CREATE_IMMIGRATION_TABLE="""
Create Table If Not Exists {}(
    uname_id      int,
    cicid         float,
    i94yr         float,
    i94mon        float,
    i94cit        float,
    i94res        float,
    i94port       varchar,
    arrdate       float,
    i94mode       float,
    i94addr       varchar,
    depdate       float,
    i94bir        float,
    i94visa       float,
    count         float,
    dtadfile      int,
    visapost      varchar,
    occup         varchar,
    entdepa       varchar,
    entdepd       varchar,
    entdepu       float,
    matflag       varchar,
    biryear       float,
    dtaddto       varchar,
    gender        varchar,
    insnum        float,
    airline       varchar,
    admnum        float,
    fltno         varchar,
    visatype      varchar
)
""".format(IMMIGRATION_TABLE)

CREATE_AIRPORT_TABLE="""
Create Table If Not Exists {}(
    ident           varchar,
    type            varchar,
    name            varchar,
    elevation_ft    float,
    continent       varchar,
    iso_country     varchar,
    iso_region      varchar,
    municipality    varchar,
    gps_code        varchar,
    iata_code       varchar,
    local_code      varchar,
    coordinates     varchar
)
""".format(AIRPORT_TABLE)


# redshift query
COPY_DEMOGRAPHICS_DATA_FROM_S3="""
copy {}
from '{}'
iam_role '{}'
region '{}'
format as csv
delimiter as ';'
ignoreheader 1;
""".format(DEMOGRAPHICS_TABLE, BUCKET+DEMOGRAPHICS_DATA, IAM_ROLE, REGION)

COPY_INFORMATION_DATA_FROM_S3="""
copy {}
from '{}'
iam_role '{}'
region '{}'
format as csv
delimiter as ','
ignoreheader 1;
""".format(IMMIGRATION_TABLE, BUCKET+IMMIGRATION_DATA, IAM_ROLE, REGION)

COPY_AIRPORT_DATA_FROM_S3="""
copy {}
from '{}'
iam_role '{}'
region '{}'
format as csv
delimiter as ','
ignoreheader 1;
""".format(AIRPORT_TABLE, BUCKET+AIRPORT_DATA, IAM_ROLE, REGION)


create_table_queries=[CREATE_DEMOGRAPHICS_TABLE, CREATE_IMMIGRATION_TABLE,CREATE_AIRPORT_TABLE]
drop_table_queries=[]
for table in TABLES:
    QUERY="""
        Drop Table If Exists {};
    """.format(table)
    drop_table_queries.append(QUERY)
    
copy_table_queries=[COPY_DEMOGRAPHICS_DATA_FROM_S3, COPY_INFORMATION_DATA_FROM_S3, COPY_AIRPORT_DATA_FROM_S3]
insert_table_queries=[]