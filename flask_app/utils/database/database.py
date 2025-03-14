import mysql.connector
import glob
import json
import csv
import os
from io import StringIO
import itertools
import datetime
class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info


    # function to insert the initial values 
    def insertValues(table): 
        return None


    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        # connect to the database 
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1')
        cursor = cnx.cursor()

        if purge:
            # drop the exisiting tables (clear the current database)
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            cnx.commit()


        # go through each sql lite file to create the tables 
        sql_files = ['flask_app/database/create_tables/feedback.sql', 'flask_app/database/create_tables/institutions.sql', 'flask_app/database/create_tables/positions.sql', 'flask_app/database/create_tables/experiences.sql', 'flask_app/database/create_tables/skills.sql']
        # go through each file 
        for file in sql_files: 
            # open the file
            with open(file, 'r') as opened_file: 
                script = opened_file.read()
                try:
                    # try to the command (create table) in the file 
                    cursor.execute(script)
                except mysql.connector.Error as err:
                    # print out the error that occured in creating the table
                    print(f"Error executing {file}: {err}")

        # insert initial values 
        csv_files = ['flask_app/database/initial_data/institutions.csv', 'flask_app/database/initial_data/positions.csv', 'flask_app/database/initial_data/experiences.csv','flask_app/database/initial_data/skills.csv']
        
        # go through all the csv files 
        for file in csv_files: 
            # get the table name 
            table = file.split('/')[-1].replace('.csv', '')
            # open the file 
            try: 
                with open(file, 'r') as opened_file: 
                    reader = csv.reader(opened_file)
                    columns = next(reader)
                    for row in reader:
                        row = [None if val == 'NULL' else val for val in row]
                        values_placeholder = ', '.join(['%s'] * len(columns))
                        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({values_placeholder})"

                        try:
                            cursor.execute(query, row)
                        except mysql.connector.Error as err:
                            print(f"Error inserting data into {table}: {err}")
            except Exception as e: 
                print("Error occured with csv file inserting: ", e)

        cnx.commit()
        cursor.close()
        cnx.close()

    
    # insert rows in a table in the database 
    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
         # create connection to the database 
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1')
        cursor = cnx.cursor()

        try:
            # write out the query
            temp = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({temp})"
            # actually do the query 
            cursor.executemany(query, parameters)
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data into {table}: {err}")

        # close connection to the database 
        cursor.close()
        cnx.close()


    def getResumeData(self):
        # connect to the database
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1')
        cursor = cnx.cursor(dictionary = True)

        resume = {}

        # get institution data 
        cursor.execute("SELECT * FROM institutions")
        institutions = cursor.fetchall()
        for place in institutions: 
            inst_id = place['inst_id']
            resume[inst_id] = {
                'name': place['name'],
                'type': place['type'],
                'department': place.get('department'),
                'address': place.get('address'),
                'city': place.get('city'),
                'state': place.get('state'),
                'zip': place.get('zip'),
                'positions': {}
            }

            # go through positions 
            cursor.execute("SELECT * FROM positions WHERE inst_id = %s", (inst_id,))
            positions = cursor.fetchall()
            for position in positions: 
                pos_id = position['position_id']
                resume[inst_id]['positions'][pos_id] = {
                    'title': position['title'],
                    'start_date': position['start_date'],
                    'end_date': position['end_date'],
                    'responsibilities': position['responsibilities'],
                    'experiences': {}
                }
            
                # go through experience table 
                cursor.execute("SELECT * FROM experiences WHERE position_id = %s", (pos_id,))
                experiences = cursor.fetchall()
                for experience in experiences: 
                    experience_id = experience['experience_id']
                    resume[inst_id]['positions'][pos_id]['experiences'][experience_id] = {
                        'name': experience['name'],
                        'description': experience['description'],
                        'start_date': experience['start_date'],
                        'end_date': experience['end_date'],
                        'hyperlink': experience.get('hyperlink'),
                        'skills': {}
                    }

                    # go through skills table
                    cursor.execute("SELECT * FROM skills WHERE experience_id = %s", (experience_id,))
                    skills = cursor.fetchall()
                    for skill in skills: 
                        skill_id = skill['skill_id']
                        resume[inst_id]['positions'][pos_id]['experiences'][experience_id]['skills'][skill_id] = {
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }

        # close connection with database 
        cursor.close()
        cnx.close()
        # format resume before returning for easier reading 
        #resume = json.dumps(resume, indent=4, default=str)
        return (resume)


    def getFeedbackRows(self): 
     # connect to the database
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1')
        cursor = cnx.cursor(dictionary = True)

        query = f"SELECT * FROM feedback"
    
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error retrieving data from feedback: {err}")
            rows = []

        cursor.close()
        cnx.close()
        return(rows)