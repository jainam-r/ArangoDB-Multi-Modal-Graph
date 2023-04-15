# Multi-Model Database Knowledge Graphs Using ArangoDB with Wikidata
--------------------

Problem Statement 1: Load the Wikidata into ArangoDB and create a graph that represents the relationships between entities, such as people, places, and things. Use AQL to query the graph and find all instances of a particular entity type, such as all instances of a person.

--------------------

Before Replicating the code given, install all the requirements in requirements.txt

## Loading the Wikidata into ArangoDB

Concerns: The Data file is too large to directly upload it to ArangoDB. Hence it has to be uploaded using a script.


Refer to wikidata dump extract.py for the same

## Create a Graph

Concerns: There are a number of properties associated with each node. Hence, a representational decision is to be made to decide the property that is to be used as an edge between some nodes. Also, the possibility of "null" values has to be handled.


