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

# def fetch_and_process_all_data(table_columns_map, question_table, csv_file_path):
#     try:
#         # Connect to the PostgreSQL database
#         cursor = connection.cursor()
        
#         dataframes = {}
        
#         # Fetch data from each specified table and store it in a DataFrame
#         for table, columns in table_columns_map.items():
#             columns_str = ', '.join([f'"{column}"' for column in columns])
#             query = f'SELECT {columns_str} FROM "{table}";'
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             df = pd.DataFrame(rows, columns=columns)
#             dataframes[table] = df
        
#         # Fetch and transform data from the question table
#         query = f'SELECT "userId", "questionId", "answer" FROM "{question_table}";'
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         df_questions = pd.DataFrame(rows, columns=['userId', 'questionId', 'answer'])
#         df_filtered = df_questions[df_questions['questionId'].isin(question_id_mapping.keys())]
#         df_filtered['column_name'] = df_filtered['questionId'].map(question_id_mapping)
#         df_grouped = df_filtered.groupby(['userId', 'column_name'])['answer'].first().reset_index()
#         df_pivot = df_grouped.pivot(index='userId', columns='column_name', values='answer').reset_index()
        
#         # Merge all DataFrames on 'userId'
#         merged_df = dataframes['personalDetails']
#         for table in ['otherDetails', 'qualificationDetails', 'locationDetails']:
#             merged_df = pd.merge(merged_df, dataframes[table], on='userId', how='inner')
        
#         # Merge with the pivoted question data
#         final_df = pd.merge(merged_df, df_pivot, on='userId', how='inner')
        
#         # Save the final DataFrame to a CSV file
#         final_df.to_csv(f'{csv_file_path}_final.csv', index=False)
        
#         print(f"Data saved to {csv_file_path}_final.csv")
#         return final_df
    
#     except Exception as e:
#         print(f"Error: {e}")

# # Define the columns to fetch from each table
# table_columns_map = {
#     'personalDetails': ['userId', 'martialStatus', 'numberOfChildren'],
#     'otherDetails': ['userId', 'caste', 'community', 'religion', 'placeOfBirth', 'smokingHabbit', 'drinkingHabbit'],
#     'qualificationDetails': ['userId', 'qualification', 'currentWorkingStatus', 'occupation', 'income'],
#     'locationDetails': ['userId', 'country', 'state']
# }

# # Define the table for questions
# question_table = 'Answers'

# # Fetch, process, and save data in one function call
# csv_file_path = 'merge'
# final_df = fetch_and_process_all_data(table_columns_map, question_table, csv_file_path)
