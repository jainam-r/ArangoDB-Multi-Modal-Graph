#Loading all the packages
import time
start_time = time.time()
from pymongo import MongoClient
from bson import ObjectId
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#Setting up a connection with MongoDB using PyMongo
try:
    uri = "mongodb+srv://jainam-r:zenteiq@cluster0.ntxqi3q.mongodb.net/?tls=true&tlsAllowInvalidCertificates=true"
    conn = MongoClient(uri)
    print("connection established!")
except Exception as e:
    raise SystemExit(1)

#From where to fetch this data?    
user_id = ObjectId('64a1b10b3bdd820e84b7353b')

#Fetching the skills user's goal and the skills he currently have from the Survey_DB
db_survey = conn['Survey']
collection_1 = db_survey['Goals']
filter = {"user_id": user_id}
results = collection_1.find(filter, {"focused_role": 1, "existing_skills": 1})
output_1 = [[result["focused_role"], result["existing_skills"]] for result in results]
user_goal = output_1[0][0]
user_existing_skills = output_1[0][1]
print(f"{user_goal}")
print(f"{user_existing_skills}\n")

#Fetching the all the skills required to achieve user's goal from the Career_DB
db_career = conn['Career']
collection_2 = db_career['career_roles']
filter = {"Role": user_goal}
results = collection_2.find(filter, {"Skills": 1})
output_2 = [[result["Skills"]] for result in results]
career_skills_needed = output_2[0][0]
print(f"{career_skills_needed}\n")

#Subtracting the skills user have from the skills required to achieve the User's goal.
#Thus,it gives the skill-gap between user's current skills and the skills he should have to achieve his goal.
for values in user_existing_skills:
    for value in career_skills_needed:
        if values == value:
            career_skills_needed.remove(values)
user_skills = {}
user_skills[user_id] = career_skills_needed
print(f"{user_skills}\n")

#Fetching all the courses and their needed fields from courses collection from coursesDB
#Formed a course_skills dictionary with its keys as Course Names and values as skills offered by that course
db_courses = conn['Courses']
collection3 = db_courses['course']
documents_courses = list(collection3.find({}, {'course_name': 1, 'skills_you_will_gain': 1}))
course_skills= {}
for document in documents_courses:
    key = document['course_name']
    value = document['skills_you_will_gain']
    if key in course_skills:
        course_skills[key].extend(value)
    else:
        course_skills[key] = value
print(f"{course_skills}\n") 

#Creating a list of all the different skills offered by all the courses
all_skills_set = set()
for skills in course_skills.values():
    all_skills_set.update(skills)
all_skills = list(all_skills_set)
print(f"{all_skills}\n")

#Forming an index for all the skills
skill_with_index_user = {}
for i, skill in enumerate(all_skills):
  skill_with_index_user[skill] = i
print(f"{skill_with_index_user}\n") 

#Forming a user vector(length = no.of skills in all skills) in which all the skills required to achieve the desired career role will be marked as 1
user_profile = np.zeros(len(all_skills))
user_profile_skills = user_skills[user_id]
for skill in user_profile_skills:
    if skill in skill_with_index_user:
        user_profile[skill_with_index_user[skill]] = 1
print(f"{user_profile_skills}\n")    
print(f"{user_profile}\n")    

#Forming a course vs all_skills matrix with rows as courses and in this all the skills offered by the courses are marked as 1 
course_representations = np.zeros((len(course_skills), len(all_skills)))
for i, skills in enumerate(course_skills.values()):
    for skill in skills:
        if skill in skill_with_index_user:
            course_representations[i, skill_with_index_user[skill]] = 1
print(f"{course_representations}\n")            

#Calculating the similarity scores of user_skills and course_skills
similarity_scores = cosine_similarity(user_profile.reshape(1, -1), course_representations)
print(f"{similarity_scores}\n")

#Sorting the scores in descending order
ranked_courses_indices = np.argsort(similarity_scores, axis=1)[0][::-1]
print(f"{ranked_courses_indices}\n")

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