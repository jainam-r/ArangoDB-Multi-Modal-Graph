# Multi-Model Database Knowledge Graphs Using ArangoDB with Wikidata
-------------------------------------------------------------------------------------

Problem Statement 1: Load the Wikidata into ArangoDB and create a graph that represents the relationships between entities, such as people, places, and things. Use AQL to query the graph and find all instances of a particular entity type, such as all instances of a person.

-------------------------------------------------------------------------------------

wikidata (https://wikidata.org) is a free collaborative, multilingual, secondary database, collecting structured data to provide support for Wikipedia, Wikimedia Commons, the other wikis of the Wikipedia movement and to anyone in thw world.

Lots of data:-
> 99M items
> 6,000 properties
> 2,000,000 classes
> 4,000 external id types

Processing Wikidata dumps is just like any `ETL job`:

`Extract` — we’ve got the raw data by now, just ingest it in your processing tool.

`Transform` — discard entities you are not interested in, and transform the entities you need into the format required for the loading phase.

`Load` — import your new clean data into your database or system of choice.

--------------------------------------------------------------------------------------

Before Replicating the code given, install all the requirements in requirements.txt

## Loading the Wikidata into ArangoDB

Concerns: The Data file is too large to directly upload it to ArangoDB. Hence it has to be uploaded using a script.

We have figured out 2 ways of extractions:-
1) python - using pyarango library (preferred)
2) nodejs - using big-json and yarn which are JSONStream packages.

Refer to 'wikidata dump extract.py' and 'wikidata.js' for the same

## Create a Graph

Concerns: There are a number of properties associated with each node. Hence, a representational decision is to be made to decide the property that is to be used as an edge between some nodes. Also, the possibility of "null" values has to be handled.


