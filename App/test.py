# from django.db import connection
# from django.http import JsonResponse
# import psycopg2
# import pandas as pd
# def get_all_databases(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
#         databases = cursor.fetchall()
        
#     # Convert the list of tuples into a list of strings
#     database_list = [db[0] for db in databases ]
    
#     return JsonResponse({'databases':database_list})



# def get_tables_from_postgres(database_name):
#     try:
#         # Connect to the postgres database
     
#         cursor = connection.cursor()
        
#         # Fetch all table names from the database
#         cursor.execute(
#             "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
#         )
#         tables = cursor.fetchall()
        
#         # Extract table names from the result
#         table_list = [table[0] for table in tables]
#         return table_list
    
#     except (Exception, psycopg2.Error) as error:
#         print(f"Error fetching tables from PostgreSQL database: {error}")
#         return []
    
#     finally:
#         # Close the database connection
#         if connection:
#             cursor.close()
#             connection.close()

# # Specify the database name
# database_name = "wedlock"
# table_list = get_tables_from_postgres(database_name)
# # print(table_list)

# # print("Tables in the postgres database:", table_list)

# # import pandas as pd
# # import psycopg2


# def fetch_all_data_from_table(table_name, csv_file_path):
#     try:
#         # Connect to the PostgreSQL database
#         cursor = connection.cursor()
        
#         dataframes = {}
        
#         # Fetch data from each table and store it in a DataFrame
#         for table in table_name:
#             query = f'SELECT * FROM "{table}";'
#             cursor.execute(query)
            
#             # Retrieve the column names
#             columns = [desc[0] for desc in cursor.description]
#             print(f"Table name {table} and columns: {columns}")
            
#             # Fetch all rows
#             rows = cursor.fetchall()
            
#             # Convert rows to a DataFrame
#             df = pd.DataFrame(rows, columns=columns)
#             dataframes[table] = df
            
#         # Start with the Users table DataFrame
#         final_df = dataframes['Users'].drop_duplicates(subset=['userId'])
        
#         # Loop through other tables and merge on 'userId' if the column exists
#         for table, df in dataframes.items():
#             if table != 'Users' and 'userId' in df.columns:
#                 final_df = pd.merge(final_df, df.drop_duplicates(subset=['userId']), on='userId', how='left', suffixes=('', f'_{table}'))
        
#         # Save the final DataFrame to CSV
#         final_df.to_csv(csv_file_path, index=False)
        
#         return final_df  # Return the final merged DataFrame
        
#     except (Exception, psycopg2.Error) as error:
#         print(f"Error fetching data from PostgreSQL table: {error}")
#         return None  # Return None in case of error
    
#     finally:
#         # Close the database connection
#         if connection:
#             cursor.close()
#             connection.close()

# # Specify the table names and fetch data
# table_name = ["Users", "locationDetails", "otherDetails", "personalDetails", "qualificationDetails", "imageUploads", "Answers", "Questions"]
# csv_file_path = "app_userprofile_data.csv"
# data = fetch_all_data_from_table(table_name, csv_file_path)
