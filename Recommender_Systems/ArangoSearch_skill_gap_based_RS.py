#Loading all the packages
import time
start_time = time.time()
from pyArango.connection import Connection
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#Setting up a connection within my local device for ArangoDB
try:
    conn = Connection(
        arangoURL='http://localhost:8529',
        username='root',
        password=''
    )
except Exception as e:
    raise SystemExit(1)

#From where to fetch this data?    
user_id = '4043792'

#Fetching the skills user's goal and the skills he currently have from the Survey_DB
db_survey = conn['Survey_DB']
query = f"""
FOR e in learning_goals
FILTER e.user_id == "{user_id}"
RETURN [e.target_role,e.existing_skills]
"""
output = db_survey.AQLQuery(query, rawResults=True)
user_goal = output[0][0]
user_existing_skills = output[0][1]

#Fetching the all the skills required to achieve user's goal from the Career_DB(i.e. Getting_Started)
db_career = conn['Getting_Started']
query_1 = f"""
FOR e in career_roles
FILTER e.role == "{user_goal}"
RETURN [e.skills]
"""
output_1 = db_career.AQLQuery(query_1, rawResults=True)
career_skills_needed = output_1[0][0]

#Subtracting the skills user have from the skills required to achieve the User's goal.
#Thus,it gives the skill-gap between user's current skills and the skills he should have to achieve his goal'''
for values in user_existing_skills:
    for value in career_skills_needed:
        if values == value:
            career_skills_needed.remove(values)
user_skills = {}
user_skills[user_id] = career_skills_needed
user_target_skills = list(user_skills.values())[0]

#Using ArangoSearch scoring schemes BM25,sorting the scores in descending order matching the user_skills
db_courses = conn['Courses_DB']
query_2 = f"""
FOR doc IN Courses_View_DB
  SEARCH ANALYZER(doc.concepts_content IN {user_target_skills}, "identity")
  SORT BM25(doc) DESC
  RETURN {{name: doc.Course_Name, score: BM25(doc)}}
"""
user_courses = db_courses.AQLQuery(query_2, rawResults=True)

#Making the top recommendations
if len(user_courses) > 0:
 print("The Courses based on the User's Target Skills are:")
 for c in user_courses:
    name = c['name']
    score = c['score']
    print(f"{name}     {score}")
else:
   print("No Courses found for the User.")    

end_time = time.time()
execution_time = end_time - start_time
print("Time: ", execution_time, "seconds")    
