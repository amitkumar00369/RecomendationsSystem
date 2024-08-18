from django.shortcuts import render
# from .serializers import userSerializer
# Create your views here.
from rest_framework.views  import APIView
# from .models import UserProfile
from rest_framework.response import Response
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# data = pd.read_csv('new_dummyFiles.csv', encoding='ISO-8859-1')
import pandas as pd
from django.db import connection
import json

# Mapping for question IDs to column names
question_id_mapping = {
    1: 'Gender',
    2: 'Looking_for',
    4: 'Wedding_goal',
    6: 'Looking_for_relation',
    7: 'My_age',
    8: 'Partner_age',
    9: 'Partner_living in australia',
    10: 'Horoscope_match',
    12: 'Interests_and_Hobbies'
}

def fetch_and_process_all_data(table_columns_map, question_table):
    try:
        # Connect to the PostgreSQL database
        cursor = connection.cursor()
        
        dataframes = {}
        
        # Fetch data from each specified table and store it in a DataFrame
        for table, columns in table_columns_map.items():
            columns_str = ', '.join([f'"{column}"' for column in columns])
            query = f'SELECT {columns_str} FROM "{table}";'
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            dataframes[table] = df
        
        # Fetch and transform data from the question table
        query = f'SELECT "userId", "questionId", "answer" FROM "{question_table}";'
        cursor.execute(query)
        rows = cursor.fetchall()
        df_questions = pd.DataFrame(rows, columns=['userId', 'questionId', 'answer'])
        df_filtered = df_questions[df_questions['questionId'].isin(question_id_mapping.keys())]
        # df_filtered['column_name'] = df_filtered['questionId'].map(question_id_mapping)
        df_filtered = df_filtered.copy() 
        df_filtered.loc[:, 'column_name'] = df_filtered['questionId'].map(question_id_mapping)

        df_grouped = df_filtered.groupby(['userId', 'column_name'])['answer'].first().reset_index()
        df_pivot = df_grouped.pivot(index='userId', columns='column_name', values='answer').reset_index()
        
        # Merge all DataFrames on 'userId'
        merged_df = dataframes['personalDetails']
        for table in ['otherDetails', 'qualificationDetails', 'locationDetails']:
            merged_df = pd.merge(merged_df, dataframes[table], on='userId', how='inner')
        
        # Merge with the pivoted question data
        final_df = pd.merge(merged_df, df_pivot, on='userId', how='inner')
        
        # Save the final DataFrame to a CSV file
        # final_df.to_csv(f'{csv_file_path}_final.csv', index=False)
        
        # print(f"Data saved to {csv_file_path}_final.csv")
        return final_df
    
    except Exception as e:
        print(f"Error: {e}")

# Define the columns to fetch from each table
# table_columns_map = {
#     'personalDetails': ['userId', 'martialStatus', 'numberOfChildren'],
#     'otherDetails': ['userId', 'caste', 'community', 'religion', 'placeOfBirth', 'smokingHabbit', 'drinkingHabbit'],
#     'qualificationDetails': ['userId', 'qualification', 'currentWorkingStatus', 'occupation', 'income'],
#     'locationDetails': ['userId', 'country', 'state']
# }

# # Define the table for questions
# question_table = 'Answers'

# # Fetch, process, and save data in one function call

# final_df = fetch_and_process_all_data(table_columns_map, question_table)

def get_filtered_recommendations(userId, top_n=5):
    # print("welcome",userId)
    # users=UserProfile.objects.all().values()
    # # print(users)
    # data=pd.DataFrame(users)
    # print("dsjkj",len(data),data.columns)
    # print(data)
    table_columns_map = {
    'personalDetails': ['userId', 'martialStatus', 'numberOfChildren'],
    'otherDetails': ['userId', 'caste', 'community', 'religion', 'placeOfBirth', 'smokingHabbit', 'drinkingHabbit'],
    'qualificationDetails': ['userId', 'qualification', 'currentWorkingStatus', 'occupation', 'income'],
    'locationDetails': ['userId', 'country', 'state']
    }

# Define the table for questions
    question_table = 'Answers'
    data=fetch_and_process_all_data(table_columns_map, question_table)
    data['Interests_and_Hobbies'] = data['Interests_and_Hobbies'].apply(
    lambda x: ", ".join(json.loads(x)) if isinstance(x, str) else x)
    # print(data.columns)
    # print("hello",data.shape)
    # data.to_csv("new_file_data.csv")
    # print(data)
    if data.empty:
        print("No user data available.")
        return Response({"message":"dataset not makeit"},400)
    # userId = userId.strip().lower()
    # print(userId)
    data['userId'] = data['userId'].astype(str)
    data['Gender'] = data['Gender'].str.strip('"')
    data['Looking_for']=data['Looking_for'].str.strip('"')
    if userId not in data['userId'].values:
        print("User ID not found.")
        return Response({"message":"dataset has no value of userId"},400)
    newDf=[]
    # Get the gender preference of the target profile
    
    # Get the gender preference of the target profile
    target_looking_for = data[data['userId'] == userId]['Looking_for'].values[0]
    print("jkjkcjkjdjd",target_looking_for) #Here is not working
    if target_looking_for=='Woman':
        filtered_indices = data[data['Gender'] == target_looking_for].index
        print("hello")
        
        for i in filtered_indices:
            newDf.append(data.iloc[[i]]) 
        df=pd.concat(newDf,ignore_index=True)
        features = ['Wedding_goal', 'Partner_living in australia', 'Horoscope_match', 
                'Interests_and_Hobbies', 'qualification', 'currentWorkingStatus', 'occupation', 
                'martialStatus', 'smokingHabbit', 'drinkingHabbit', 'caste', 'community', 'religion',
                'placeOfBirth','numberOfChildren','country']
    
    # Combine features into a single string for text processing
        df['combined_features'] = df[features].apply(lambda row: ','.join(row.values.astype(str)), axis=1)
        print(df['Gender'])
        
        
    
    
    # Vectorize the combined features
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['combined_features'])
       
    
    # Compute the similarity matrix
        similarity_matrix = cosine_similarity(X)

    # Extract the user’s features and vectorize them
        user_idx = data[data['userId'] == userId].index[0]
        user_features = ','.join(data.loc[user_idx, features].astype(str))
        # print("gvhjbh",user_features)
        user_vector = vectorizer.transform([user_features])

    # Calculate similarity between the user and all profiles in the dataset
        user_similarity_scores = cosine_similarity(user_vector, X).flatten()
#         print("bjjkd",user_similarity_scores)

    # Get similarity scores and sort them
        similarity_scores = list(enumerate(user_similarity_scores))
        sorted_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
#         print("sorted_user",sorted_users)

    # If there are fewer users than top_n, adjust top_n
        top_n = min(top_n, len(sorted_users) - 1)

    # Get the recommended users' IDs and their similarity percentages
        recommendations = [
        {
            'userId': df.iloc[i[0]]['userId'],
            'similarity_percentage': i[1] * 100  # Convert similarity to percentage
        }
        for i in sorted_users[1:top_n+1]  # Skip the first user which is the user itself
        ]
    

    
    elif target_looking_for=='Man':
        print("welcome")
        filtered_indices = data[data['Gender'] == target_looking_for].index
        print(filtered_indices)
        for i in filtered_indices:
            newDf.append(data.iloc[[i]]) 
#             print("jkjnd",newDf)
        df=pd.concat(newDf,ignore_index=True)
        # print("hello",df.columns)
        features = ['Wedding_goal', 'Partner_living in australia', 'Horoscope_match', 
                'Interests_and_Hobbies', 'qualification', 'currentWorkingStatus', 'occupation', 
                'martialStatus', 'smokingHabbit', 'drinkingHabbit', 'caste', 'community', 'religion',
                'placeOfBirth','numberOfChildren','country']
    
    # Combine features into a single string for text processing
        df['combined_features'] = df[features].apply(lambda row: ','.join(row.values.astype(str)), axis=1)
        
        
    
    
    # Vectorize the combined features
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['combined_features'])
    
    # Compute the similarity matrix
        similarity_matrix = cosine_similarity(X)

    # Extract the user’s features and vectorize them
        user_idx = data[data['userId'] == userId].index[0]
        user_features = ','.join(data.loc[user_idx, features].astype(str))
        # print("gvhjbh",user_features)
        user_vector = vectorizer.transform([user_features])

    # Calculate similarity between the user and all profiles in the dataset
        user_similarity_scores = cosine_similarity(user_vector, X).flatten()
#         print("bjjkd",user_similarity_scores)

    # Get similarity scores and sort them
        similarity_scores = list(enumerate(user_similarity_scores))
        sorted_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
#         print("sorted_user",sorted_users)

    # If there are fewer users than top_n, adjust top_n
        top_n = min(top_n, len(sorted_users) - 1)

    # Get the recommended users' IDs and their similarity percentages
        recommendations = [
        {
            'userId': df.iloc[i[0]]['userId'],
            'similarity_percentage': i[1] * 100  # Convert similarity to percentage
        }
        for i in sorted_users[1:top_n+1]  # Skip the first user which is the user itself
        ]
    

    


# 
    
    # Get top N recommendations, excluding the p
    
    else:
        features = ['Wedding_goal', 'Partner_living in australia', 'Horoscope_match', 
                'Interests_and_Hobbies', 'qualification', 'currentWorkingStatus', 'occupation', 
                'martialStatus', 'smokingHabbit', 'drinkingHabbit', 'caste', 'community', 'religion',
                'placeOfBirth','numberOfChildren','country']
        data['combined_features'] = data[features].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# One-hot encode the categorical features
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(data['combined_features'])

# Calculate cosine similarity between all users
        similarity_matrix = cosine_similarity(X)
        user_idx = data[data['userId'] == userId].index[0]
       
    
    # Get similarity scores for the user
        similarity_scores = list(enumerate(similarity_matrix[user_idx]))
    
    # Sort the users based on similarity scores (excluding the user itself)
        sorted_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # If there are fewer users than top_n, adjust top_n
        top_n = min(top_n, len(sorted_users) - 1)
    
    # Get the recommended users' IDs and their similarity percentages
        recommendations = [
        {
            'userId': data.iloc[i[0]]['userId'],
            'similarity_percentage': i[1] * 100  # Convert similarity to percentage
        }
        for i in sorted_users[1:top_n+1]  # Skip the first user which is the user itself
        ]
    # print(recommendations)
    
    return recommendations
        
# filtered_recommendations = get_filtered_recommendations("a76626b1-44cc-48e7-b87a-d84cc0e8416e", top_n=5)
# filtered_recommendations
# # filtered_recommendations
# frame = []
# for i in range(len(filtered_recommendations)):
#     print(f"user precentage = {filtered_recommendations[i]['similarity_percentage']}%, and this is userId = {filtered_recommendations[i]['userId']}")
#     frame.append(data[data['userId'] == filtered_recommendations[i]['userId']])

# # Concatenate all DataFrames in the list into a single DataFrame
# df_new1 = pd.concat(frame, ignore_index=True)

# # Display the new DataFrame
# df_new1
class View(APIView):
    def get(self,request,userId:None):
       
        try:
            print(userId)
            if not isinstance(userId, str):
                return Response({'message': "userId must be a string"}, status=400)
            
            if not userId:
                return Response({"Enter userId"})
            value=get_filtered_recommendations(userId=userId)
            
            
            return Response({'message':"success","data":value},200)
        except Exception as e:
            return Response(str(e))
            
    