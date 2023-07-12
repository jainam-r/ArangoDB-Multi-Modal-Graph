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
print(user_existing_skills)

#Fetching the all the skills required to achieve user's goal from the Career_DB(i.e. Getting_Started)
db_career = conn['Getting_Started']
query_1 = f"""
FOR e in career_roles
FILTER e.role == "{user_goal}"
RETURN [e.skills]
"""
output_1 = db_career.AQLQuery(query_1, rawResults=True)
career_skills_needed = output_1[0][0]
print(career_skills_needed)

#Subtracting the skills user have from the skills required to achieve the User's goal.
#Thus,it gives the skill-gap between user's current skills and the skills he should have to achieve his goal'''
for values in user_existing_skills:
    for value in career_skills_needed:
        if values == value:
            career_skills_needed.remove(values)
user_skills = {}
user_skills[user_id] = career_skills_needed
print(user_skills)

#Fetching all the courses and their needed fields from courses collection from coursesDB
#Formed a course_skills dictionary with its keys as Course Names and values as skills offered by that course
db_courses = conn['Courses_DB']
collection1 = db_courses['courses']
documents_courses = collection1.fetchAll(fields = ['Course_Name','concepts_content'])
course_skills= {}
for document in documents_courses:
    key = document['Course_Name']
    value = document['concepts_content']
    if key in course_skills:
        course_skills[key].extend(value)
    else:
        course_skills[key] = value
print(course_skills)        

#Creating a list of all the different skills offered by all the courses
all_skills_set = set()
for skills in course_skills.values():
    all_skills_set.update(skills)
all_skills = list(all_skills_set)
print(all_skills)

#Forming an index for all the skills
skill_with_index_user = {}
for i, skill in enumerate(all_skills):
  skill_with_index_user[skill] = i
print(skill_with_index_user) 

#Forming a user vector(length = no.of skills in all skills) in which all the skills required to achieve the desired career role will be marked as 1
user_profile = np.zeros(len(all_skills))
user_profile_skills = user_skills[user_id]
for skill in user_profile_skills:
    if skill in skill_with_index_user:
        user_profile[skill_with_index_user[skill]] = 1
print(user_profile_skills)        

#Forming a course vs all_skills matrix with rows as courses and in this all the skills offered by the courses are marked as 1 
course_representations = np.zeros((len(course_skills), len(all_skills)))
for i, skills in enumerate(course_skills.values()):
    for skill in skills:
        if skill in skill_with_index_user:
            course_representations[i, skill_with_index_user[skill]] = 1
print(course_representations)            

#Calculating the similarity scores of user_skills and course_skills
similarity_scores = cosine_similarity(user_profile.reshape(1, -1), course_representations)
print(similarity_scores)

#Sorting the scores in descending order
ranked_courses_indices = np.argsort(similarity_scores, axis=1)[0][::-1]
print(ranked_courses_indices)

#Making the top 5 scores recommendations
print("Top 5 Recommended Courses for User:")
Suggested_courses = []
for index in ranked_courses_indices:
    course_name = list(course_skills.keys())[index]
    similarity_score = similarity_scores[0, index]
    a = (f"{course_name} ({similarity_score})")
    Suggested_courses.append(a)
    
Top_suggested_courses = Suggested_courses[:5]
for element in Top_suggested_courses:
  print(element)

end_time = time.time()
execution_time = end_time - start_time
print("Time: ", execution_time, "seconds")    
