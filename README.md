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

Variables to be Modified are:
`LIMIT` - This specifies the number of objects to be extracted from the wikidata. More the data, more the time taken to process it.

`URL` - This specifies the location of the wikidata, any size of file can be used since we will use the url to extract the object instead of saving such large files locally.

`USERNAME` - This is the username of the ArangoDB Server of the user.

`PASSWORD` - This is the username of the ArangoDB Server of the user.

`DB_NAME` - Database Name

`ITEM_COLLECTION` - Name of collection that will store item objects.

`PROP_COLLECTION` - Name of collection that will store property objects.

`EDGE_COLLECTION` - Name of collection that will store edges between items and properties.

Before Replicating the code given, install all the requirements in requirements.txt

Start the ArangoDB Server before running the code. PORT 8529 (Default)

