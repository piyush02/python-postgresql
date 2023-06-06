# Database Parameter Store and PostgreSQL Connection

This script retrieves database connection parameters from AWS Systems Manager Parameter Store and establishes a connection to a PostgreSQL database using psycopg2 library.

## Prerequisites

- Python 3.x
- psycopg2 library (`pip install psycopg2`)
- boto3 library (`pip install boto3`)

## Usage

1. Make sure you have the necessary AWS credentials and permissions to access Systems Manager Parameter Store.

2. Set the required parameters in the script:

   - `-r` or `--region`: AWS Region where the Parameter Store and database are located.
   - `-e` or `--env`: Environment name or identifier.

3. Run the script using the following command:

   ```shell
   python3 database_parameter_store.py -r <AWS_REGION> -e <ENVIRONMENT>

Replace <AWS_REGION> with the desired AWS Region and <ENVIRONMENT> with the environment name.

The script will retrieve the specified parameters from AWS Systems Manager Parameter Store and establish a connection to the PostgreSQL database.
Script Details

The script consists of the following classes and functions:
parameter_store

This class retrieves parameter values from AWS Systems Manager Parameter Store.

    The script uses argparse to parse command-line arguments and retrieve the AWS Region and environment name.
    The AWS Region and environment name are used to construct the path to the parameter in Parameter Store.
    The boto3 library is used to interact with AWS Systems Manager and retrieve the parameter values.
    Methods in this class retrieve different parameter values, such as the database usernames, passwords, and URLs.

MyDatabase

This class establishes a connection to the PostgreSQL database using the retrieved parameter values.

    The class inherits from parameter_store to access the parameter values.
    The PostgreSQL connection is established using the psycopg2 library.
    The class contains methods to execute SQL queries, create users, and check users in the database.
    The SQL queries are stored as multiline strings within the script.

main

The main function is the entry point of the script.

    It creates an instance of the MyDatabase class and demonstrates the usage of different methods.
    The connection to the database is established, and various SQL queries and user creation operations are executed.
    Finally, the connection is closed.

Error Handling

The script incorporates basic error handling:

    If any error occurs while retrieving the parameter values or establishing the database connection, an error message will be displayed.

    The script will exit with a non-zero exit code (1).

    Ensure that you have the necessary AWS credentials and permissions to access Systems Manager Parameter Store.

    Verify that the correct AWS Region and environment name are provided as command-line arguments.

    Make sure the required Python packages (psycopg2 and boto3) are installed.
