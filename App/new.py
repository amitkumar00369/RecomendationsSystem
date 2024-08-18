# import pandas as pd
# from django.db import connection

# # Mapping for question IDs to column names
# question_id_mapping = {
#     1: 'Gender',
#     2: 'Looking_for',
#     4: 'Wedding_goal',
#     6: 'Looking_for_relation',
#     7: 'My_age',
#     8: 'Partner_age',
#     9: 'Partner_age',
#     10: 'Horoscope_match',
#     12: 'Interests_and_Hobbies'
# }

# def fetch_and_transform_data(table_name, csv_file_path):
#     try:
#         # Create a cursor object using Django's connection
#         with connection.cursor() as cursor:
#             # Fetch the data from the specified table, quoting column names to preserve case
#             query = f'SELECT "userId", "questionId", "answer" FROM "{table_name}";'
#             cursor.execute(query)
            
#             # Fetch all rows
#             rows = cursor.fetchall()
        
#         # Convert rows to a DataFrame
#         df = pd.DataFrame(rows, columns=['userId', 'questionId', 'answer'])
        
#         # Filter the DataFrame to include only the relevant questionIds
#         df_filtered = df[df['questionId'].isin(question_id_mapping.keys())]
        
#         # Use .loc to avoid SettingWithCopyWarning
#         df_filtered.loc[:, 'column_name'] = df_filtered['questionId'].map(question_id_mapping)
        
#         # Handle duplicate entries by aggregating (e.g., taking the first answer for each combination)
#         df_grouped = df_filtered.groupby(['userId', 'column_name'])['answer'].first().reset_index()
        
#         # Pivot the DataFrame to get questionId as columns
#         df_pivot = df_grouped.pivot(index='userId', columns='column_name', values='answer')
        
#         # Reset index to make userId a column
#         df_pivot = df_pivot.reset_index()
        
#         # Save the transformed data to a CSV file
#         df_pivot.to_csv(csv_file_path, index=False)
#         print(f"Data saved to {csv_file_path}")
        
#     except Exception as error:
#         print(f"Error fetching data from PostgreSQL: {error}")

# # Usage
# table_name = "Answers"
# csv_file_path = "app_userprofile_data.csv"

# # Fetch, transform, and save data in one function call
# fetch_and_transform_data(table_name, csv_file_path)

# def fetch_all_data_from_table(table_name, csv_file_path):
#     try:
#         # Connect to the PostgreSQL database
#         cursor = connection.cursor()
        
#         dataframes = {}
        
#         # Fetch data from each table and store it in a DataFrame
#         for table in table_name:
#             # Modify the query to select only specific columns
#             query = f'SELECT "userId", "martialStatus", "numberOfChildren" FROM "{table}";'
#             cursor.execute(query)
            
#             # Retrieve the column names
#             columns = [desc[0] for desc in cursor.description]
#             print(f"Table name {table} and columns: {columns}")
            
#             # Fetch all rows
#             rows = cursor.fetchall()
            
#             # Convert rows to a DataFrame
#             df = pd.DataFrame(rows, columns=columns)
#             dataframes[table] = df
            
#             # Save the DataFrame to a CSV file
#             df.to_csv(f'{csv_file_path}_{table}.csv', index=False)
        
#         return dataframes
    
#     except Exception as e:
#         print(f"Error: {e}")
# table_name = ['personalDetails']
# csv_file_path = 'persionalDetails_data'

# fetch_all_data_from_table(table_name, csv_file_path)

# def fetch_selected_data_from_tables(table_columns_map, csv_file_path):
#     try:
#         # Connect to the PostgreSQL database
#         cursor = connection.cursor()
        
#         dataframes = {}
        
#         # Fetch data from each table and store it in a DataFrame
#         for table, columns in table_columns_map.items():
#             # Convert the columns list to a string for the SQL query
#             columns_str = ', '.join([f'"{column}"' for column in columns])
#             query = f'SELECT {columns_str} FROM "{table}";'
#             cursor.execute(query)
            
#             # Print the columns for debugging
#             print(f"Table name {table} and columns: {columns}")
            
#             # Fetch all rows
#             rows = cursor.fetchall()
            
#             # Convert rows to a DataFrame
#             df = pd.DataFrame(rows, columns=columns)
#             dataframes[table] = df
        
#         # Merge DataFrames on 'userId'
#         merged_df = dataframes['personalDetails']
#         for table in ['otherDetails', 'qualificationDetails', 'locationDetails']:
#             merged_df = pd.merge(merged_df, dataframes[table], on='userId', how='inner')
        
#         # Save the merged DataFrame to a CSV file
#         merged_df.to_csv(f'{csv_file_path}_merged.csv', index=False)
        
#         return merged_df
    
#     except Exception as e:
#         print(f"Error: {e}")

# # Define the columns to fetch from each table
# table_columns_map = {
#     'personalDetails': ['userId', 'martialStatus', 'numberOfChildren'],
#     'otherDetails': ['userId', 'caste', 'community', 'religion', 'placeOfBirth', 'smokingHabbit', 'drinkingHabbit'],
#     'qualificationDetails': ['userId', 'qualification', 'currentWorkingStatus', 'occupation', 'income'],
#     'locationDetails': ['userId', 'country', 'state']
# }

# # Fetch data from the tables and save to CSV file
# csv_file_path = 'merge'
# fetch_selected_data_from_tables(table_columns_map, csv_file_path)