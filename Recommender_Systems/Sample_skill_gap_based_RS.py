import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

user_skills = {
    'User': ['Statistics', 'Linear Algebra','CSS'] }

course_skills = {
'Course 1': ['Python', 'DSA', 'Algorithms'],
'Course 2': ['Web Development', 'HTML', 'CSS', 'Algorithms'],
'Course 3': ['Data Analysis', 'Statistics', 'Machine Learning', 'Python'],
'Course 4': ['Database Management', 'SQL', 'NoSQL'],
'Course 5': ['Statistics', 'Linear Algebra'],
'Course 6': ['JavaScript', 'React', 'Front-end Development'],
'Course 7': ['Data Science', 'R', 'Data Visualization'],
'Course 8': ['Network Security', 'Cybersecurity', 'Encryption'],
'Course 9': ['Artificial Intelligence', 'Machine Learning', 'Neural Networks'],
'Course 10': ['Mobile App Development', 'Android', 'Java'],
'Course 11': ['Computer Networks', 'TCP/IP', 'Routing'],
'Course 12': ['Software Engineering', 'Agile Methodology', 'UML'],
'Course 13': ['Data Mining', 'Clustering', 'Association Rules'],
'Course 14': ['Operating Systems', 'Linux', 'Process Scheduling'],
'Course 15': ['Digital Marketing', 'SEO', 'Social Media Advertising'],
'Course 16': ['Blockchain', 'Smart Contracts', 'Cryptocurrency'],
'Course 17': ['Cloud Computing', 'AWS', 'Azure'],
'Course 18': ['Computer Graphics', 'OpenGL', '3D Modeling'],
'Course 19': ['Embedded Systems', 'Microcontrollers', 'Firmware'],
'Course 20': ['Data Analysis', 'Machine Learning','Robotics','DSA'],
'Course 21': ['Natural Language Processing', 'Python', 'Machine Learning'],
'Course 22': ['Information Security', 'Penetration Testing', 'Cybersecurity'],
'Course 23': ['Data Visualization', 'Tableau', 'Data Analytics'],
'Course 24': ['Full-Stack Web Development', 'Node.js', 'MongoDB', 'React'],
'Course 25': ['Artificial Intelligence', 'Deep Learning', 'Computer Vision'],
'Course 26': ['iOS App Development', 'Swift', 'Objective-C'],
'Course 27': ['Software Testing', 'Quality Assurance', 'Test Automation'],
'Course 28': ['Data Engineering', 'ETL', 'Big Data'],
'Course 29': ['Network Administration', 'Cisco', 'Firewalls'],
'Course 30': ['Digital Photography', 'Adobe Photoshop', 'Composition'],
'Course 31': ['UI/UX Design', 'Wireframing', 'Prototyping'],
'Course 32': ['DevOps', 'Docker', 'Continuous Integration'],
'Course 33': ['Business Analysis', 'Requirements Gathering', 'Process Improvement'],
'Course 34': ['Computer Vision', 'Image Processing', 'Pattern Recognition'],
'Course 35': ['Game Development', 'Unity', 'C#'],
'Course 36': ['Information Retrieval', 'Search Engines', 'Text Mining'],
'Course 37': ['Internet of Things', 'Arduino', 'Sensors'],
'Course 38': ['Embedded Linux', 'Yocto Project', 'Device Drivers'],
'Course 39': ['Cloud Architecture', 'Google Cloud', 'Kubernetes'],
'Course 40': ['Machine Learning for Finance', 'Time Series Analysis', 'Risk Modeling'],
'Course 41': ['Data Governance', 'Data Privacy', 'Compliance'],
'Course 42': ['Augmented Reality', 'Unity', 'ARKit'],
'Course 43': ['Quantum Computing', 'Qubits', 'Quantum Algorithms'],
'Course 44': ['IT Project Management', 'Agile', 'Scrum'],
'Course 45': ['Ethical Hacking', 'Vulnerability Assessment', 'Social Engineering'],
'Course 46': ['Data Warehousing', 'Dimensional Modeling', 'ETL'],
'Course 47': ['Bioinformatics', 'Genomics', 'Sequence Alignment'],
'Course 48': ['Robotic Process Automation', 'UiPath', 'Process Mining'],
'Course 49': ['Deep Reinforcement Learning', 'Neural Networks', 'Reinforcement Learning'],
'Course 50': ['Computer Architecture', 'Microprocessors', 'Assembly Language']
}    

m = set()
for skills in course_skills.values():
 for skill in skills:
    m.add(skill)
all_skills = list(m)
print(all_skills)

skill_with_index_user = {}
for i, skill in enumerate(all_skills):
  skill_with_index_user[skill] = i
print(skill_with_index_user)

user_profile = np.zeros(len(all_skills))
user_profile_skills = user_skills['User']
print(user_profile_skills)

for skill in user_profile_skills:
    if skill in skill_with_index_user:
        user_profile[skill_with_index_user[skill]] = 1
print(user_profile)       

course_representations = np.zeros((len(course_skills), len(all_skills)))
print(course_skills)

for i, skills in enumerate(course_skills.values()):
    for skill in skills:
        if skill in skill_with_index_user:
            course_representations[i, skill_with_index_user[skill]] = 1
print(course_representations)

similarity_scores = cosine_similarity(user_profile.reshape(1, -1), course_representations)
print(similarity_scores)

ranked_courses_indices = np.argsort(similarity_scores, axis=1)[0][::-1]
print(ranked_courses_indices)
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