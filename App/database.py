import pandas as pd
from django.db import connection
from django.http import JsonResponse

def fetch_specific_data(csv_file_path):
    try:
        # Connect to the postgres database
        cursor = connection.cursor()

        # Queries to fetch data from relevant tables
        queries = {
            "Users": 'SELECT DISTINCT ON ("userId") "userId" FROM "Users";',
            "locationDetails": '''SELECT "userId", "state" AS "Looking For", 
                                  "austrailanVisaStatus" AS "Partner Living in Australia" 
                                  FROM "locationDetails";''',
            "otherDetails": '''SELECT "userId", "caste" AS "Caste", "community" AS "Community", 
                               "religion" AS "Religion", "height" AS "Height", "weight" AS "Weight", 
                               "smokingHabbit" AS "Smoking Habits", "drinkingHabbit" AS "Drinking Habits", 
                               "diet" AS "Eating Habits" FROM "otherDetails";''',
            "personalDetails": '''SELECT "userId", "martialStatus" AS "Marital Status" 
                                  FROM "personalDetails";''',
            "qualificationDetails": '''SELECT "userId", "qualification" AS "Qualification", 
                                        "currentWorkingStatus" AS "Working Status", "occupation" AS "Occupation", 
                                        "income" AS "Income" FROM "qualificationDetails";''',
            "Answers": '''SELECT "userId", "answer" AS "Horoscope Match" 
                          FROM "Answers" 
                          WHERE "questionId" = (SELECT "id" FROM "Questions" WHERE "question" = 'Horoscope Match');'''
        }

        # Dictionary to store dataframes
        dataframes = {}

        # Execute queries and store data in DataFrames
        for table, query in queries.items():
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            dataframes[table] = df

        # Initialize the final DataFrame with 'Users' table data
        final_df = dataframes['Users']

        # Merge DataFrames based on 'userId', skip tables without 'userId'
        for table, df in dataframes.items():
            if 'userId' in df.columns and table != 'Users':
                final_df = pd.merge(final_df, df, on='userId', how='left', suffixes=('', f'_{table}'))

        # Drop duplicate 'userId'
        final_df.drop_duplicates(subset='userId', inplace=True)

        # Save the final DataFrame to CSV
        final_df.to_csv(csv_file_path, index=False)

        return final_df  # Return the final merged DataFrame

    except Exception as error:
        print(f"Error fetching data from PostgreSQL table: {error}")
        return None  # Return None in case of error

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()

# Specify the output CSV file path and fetch data
csv_file_path = "filtered_userprofile_data.csv"
data = fetch_specific_data(csv_file_path)
