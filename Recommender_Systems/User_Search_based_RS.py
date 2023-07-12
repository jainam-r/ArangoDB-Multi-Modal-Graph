#Loading all the packages
import time
start_time = time.time()
import numpy as np
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Setting up a connection with MongoDB using PyMongo
try:
    uri = "mongodb+srv://jainam-r:@cluster0.ntxqi3q.mongodb.net/?tls=true&tlsAllowInvalidCertificates=true"
    conn = MongoClient(uri)
    print("connection established!")
except Exception as e:
    raise SystemExit(1)

#Fetching the data from the courseDB collection i.e.course
db_courses = conn['Courses']
collection = db_courses['course']

#Setting up the encoder
vectorizer = TfidfVectorizer()

#Fetching the specific fields from the collection course
documents_courses = list(collection.find({}, {'course_name': 1, 'course_description': 1, 'skills_you_will_gain': 1, 'author_id': 1}))
print(f"The courses are:\n{documents_courses}\n")
course_descriptions = []
author_names = []
skills_you_will_gain = []

#Taking out the relevant values of the fields such as course description etc.
for doc in documents_courses:
    course_descriptions.append(doc['course_description'])
    author_id = doc['author_id']
    filter = {"_id": author_id}
    author = db_courses['Author'].find_one(filter, {"Instructor_name": 1})
    author_name = author['Instructor_name'].split()
    # Adding the split author name as a list to the author_names list
    author_names.append(author_name)
    skills_you_will_gain.append(doc['skills_you_will_gain'])

#Keeping the course_name track by index
course_name = [doc['course_name'] for doc in documents_courses]
print(f"Name of all the courses:\n{course_name}\n")

#Combining the course description,author names,skills user will gain for a course in a string for each course
course_author_skills = [f"{desc} {author} {skills}" for desc, author, skills in zip(course_descriptions, author_names, skills_you_will_gain)]
print(f"Combined course_author_skills list:\n{course_author_skills}\n")

#Encoding the course_author_skills using Tfidf vectorizer
tfidf_matrix = vectorizer.fit_transform(course_author_skills)
course_encoded = tfidf_matrix.toarray()
print("TF-IDF matrix for course names:\n")
print(f"{course_encoded}\n")
print(f"TF-IDF matrix shape:\n{course_encoded.shape}\n")

#This is the user's search query
user_query = "Data Science by Amarnath Gupta"

#Encoding the user's query using the Tfidf vectorizer
encoded_query = vectorizer.transform([user_query]).toarray()
print(f"TF-IDF vector for user's query:\n{encoded_query}\n")

# Find most relevant courses by finding the query cluster and then taking the similarity scores with course
relevant_courses = []
for i, course in enumerate(documents_courses):
    course_vector = course_encoded[i]
    similarity_score = cosine_similarity(encoded_query, course_vector.reshape(1, -1))[0][0]
    relevant_courses.append((course, similarity_score))

# Sorting relevant courses based on similarity scores
relevant_courses = sorted(relevant_courses, key=lambda x: x[1], reverse=True)

# Sorting the most relevant courses
recommended_courses = []
for course, similarity in relevant_courses:
    if similarity > 0.1:
        recommended_courses.append((course['course_name'], similarity))

if recommended_courses:
    print("The Top Courses found are:")
    for course, similarity in recommended_courses:
        print(course)
else:
    print("No recommendations found.")

print("\nElapsed time: %.2f seconds" % (time.time() - start_time))
