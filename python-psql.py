#!/bin/python

import psycopg2
import boto3
import argparse
from psycopg2 import Error

class parameter_store:
    parser = argparse.ArgumentParser(description="Enter parameters")
    parser.add_argument('-r', '--region', help='AWS Region', nargs='?', required=True)
    parser.add_argument('-e', '--env', help='Environment Name', nargs='?', required=True)
    args = parser.parse_args()
    AWS_REGION = args.region
    env = args.env
    ssm = boto3.client('ssm', region_name=AWS_REGION)

    def __init__(self, path_ssm):
        self.path_ssm = path_ssm

    
    def tem_flyway_user(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value'])
        except (Exception, Error) as error:
            print("Error while getting parameter value tem_flyway_user", error)
            exit(1)
    
    def tem_ops_user(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value'])
        except (Exception, Error) as error:
            print("Error while getting parameter value tem_ops_user", error)
            exit(1)
    
    def tem_app_user(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value']) 
        except (Exception, Error) as error:
            print("Error while getting parameter value tem_app_user", error)
            exit(1)
    
    def rds_url(self):
        try:    
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            rds_endpoint = (parameter['Parameter']['Value'])
            return rds_endpoint.split(':')[2].replace("//", "")
        except (Exception, Error) as error:
            print("Error while getting parameter value rds_url", error)
            exit(1)
    
    def rds_username(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value']) 
        except (Exception, Error) as error:
            print("Error while getting parameter value rds_username", error)
            exit(1)

    def rds_db_name(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value'])
        except (Exception, Error) as error:
            print("Error while getting parameter value rds_db_name", error)
            exit(1)
    
    def rds_password(self):
        try:
            parameter = self.ssm.get_parameter(Name= self.path_ssm, WithDecryption=True)
            return (parameter['Parameter']['Value']) 
        except (Exception, Error) as error:
            print("Error while getting to parameter value rds_password", error)
            exit(1)
        
### Parameter location ###

tem_flyway_user = parameter_store('/'+parameter_store.env+'/database/password/tem_flyway_user')
tem_ops_user = parameter_store('/'+parameter_store.env+'/database/password/tem_ops_user')
tem_app_user = parameter_store('/config/tem-integrations-service-'+parameter_store.env+'/spring.datasource.persist.password')
rds_url = parameter_store('/config/tem-integrations-service-'+parameter_store.env+'/spring.datasource.persist.persistUrl')
rds_username = parameter_store('/'+parameter_store.env+'/database/master/username')
rds_db_name = parameter_store('/'+parameter_store.env+'/database/name')
rds_password = parameter_store('/'+parameter_store.env+'/database/password/master')
# print(rds_url.rds_url())


class MyDatabase(parameter_store):
    #print(rds_db_name.rds_db_name())

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
            database= rds_db_name.rds_db_name(),
            user= rds_username.rds_username(),
            password= rds_password.rds_password(),
            host= rds_url.rds_url(),
            port= '5432'
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
           
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            exit(1)

       
    
    def query(self, query):
        self.cursor.execute(query)
        print(self.cursor.fetchall())
       
       
    
    def user_create(self, user_create):
        self.cursor.execute(user_create)
        print("User has been created successfully !!")
       
    
    def check_user(self, check_user):
        self.cursor.execute(check_user)
        print(self.cursor.fetchall())
       
    # def check_tem_flyway_user(self, sql):
    #     self.conn_check_tem_flyway_user = psycopg2.connect(
    #     database=rds_db_name.rds_db_name(),
    #     	user="tem_flyway_user", 
    #     	password=tem_flyway_user.tem_flyway_user(),
    #     	host='localhost',
    #     	port= '8080'
    #     )

    #     self.cursor_tem_flyway_user = self.conn_check_tem_flyway_user.cursor()
    
    # #def query_check_tem_flyway_user(self, query_check_tem_flyway_user):
    #     self.cursor_tem_flyway_user.execute(sql)
    #     print(self.cursor_tem_flyway_user.fetchall())
    #     print("tem_flyway_user")
    #     self.cursor_tem_flyway_user.close()
    #     self.conn_check_tem_flyway_user.close()
   
    
    def close(self):
        self.cursor.close()
        self.conn.close()

def main():
 
    MyDatabase()
    MyDatabase().query(sql_version)
    MyDatabase().user_create(sql_user_create)
    MyDatabase().check_user(sql_print_user)
    MyDatabase().close()
     
##### sql query #####

sql_version = f"""
SELECT version();
"""

sql_print_user = f"""
SELECT usename FROM pg_catalog.pg_user;
"""

sql_user_create = f"""
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'tem_flyway_user') THEN

      RAISE NOTICE 'Role "tem_flyway_user" already exists. Skipping.';
   ELSE
      CREATE ROLE tem_flyway_user LOGIN PASSWORD '{tem_flyway_user.tem_flyway_user()}';
      GRANT ALL ON DATABASE {rds_db_name.rds_db_name()} TO tem_flyway_user;
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'tem_app_user') THEN

      RAISE NOTICE 'Role "tem_app_user" already exists. Skipping.';
   ELSE
      CREATE ROLE tem_app_user LOGIN PASSWORD '{tem_app_user.tem_app_user()}';
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'tem_ops_user') THEN

      RAISE NOTICE 'Role "tem_ops_user" already exists. Skipping.';
   ELSE
      CREATE ROLE tem_ops_user LOGIN PASSWORD '{tem_ops_user.tem_ops_user()}';
   END IF;
END
$do$;
"""

if __name__=="__main__":
    main()
