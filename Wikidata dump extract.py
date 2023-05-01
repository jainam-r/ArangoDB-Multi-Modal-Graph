import json
import gzip
import requests
# import ast
from urllib.request import urlopen
import pyArango.connection as CON
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field, Edges

USERNAME = 'root'
PASSWORD = ''
DB_NAME = 'test1'
ITEM_COLLECTION = 'final_item'
PROP_COLLECTION = 'final_prop'
EDGE_COLLECTION = 'final_edge'
GRAPH = 'final_graph'
LIMIT = 40000 # THIS DENOTES THE TOTAL NUMBER OF OBJECTS TO BE ACCESSED FROM THE WIKIDATA
url = 'https://archive.org/download/wikidata-json-20141027/20141027.json.gz'


class read_remote_gzip(object):
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.conn = urlopen(self.url)
        self.fh = gzip.GzipFile(fileobj=self.conn)
        return self

    def __exit__(self, *exc_info):
        self.fh.close()
        self.conn.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.fh.readline()

            
item_dct = []
prop_dct = []
prop_lst = []
invalid_item = 0
invalid_prop = 0
with read_remote_gzip(url) as r:
    for ii, ln in enumerate(r):
        if ln == b'[\n' or ln == b']\n':
            continue
        if ln.endswith(b',\n'): # all but the last element
            entity_dict = json.loads(ln[:-2])
        else:
            entity_dict = json.loads(ln)
        if entity_dict['type']=='property':
            try:
                a = entity_dict['labels']['en']['value']
                b = entity_dict['descriptions']['en']['value']
#                 a = entity_dict['labels']
#                 b = entity_dict['descriptions']
                prop_lst.append(entity_dict['id'])
            except:
                c = 1
        if ii == LIMIT: break
            
with read_remote_gzip(url) as r:           
    for ii, ln in enumerate(r):
        if ln == b'[\n' or ln == b']\n':
            continue
        if ln.endswith(b',\n'): # all but the last element
            entity_dict = json.loads(ln[:-2])
        else:
            entity_dict = json.loads(ln)
        dct = {}
        if ii>LIMIT:
            break
        if entity_dict['type']=='item':
            try:
                dct['_key'] = entity_dict['id']
                dct['type'] = entity_dict['type']
                dct['label'] = entity_dict['labels']['en']['value']
#                 dct['label'] = entity_dict['labels']
                dct['description'] = entity_dict['descriptions']['en']['value']
#                 dct['description'] = entity_dict['descriptions']
                aa = entity_dict['claims'].keys()
                temp = []
                for j in aa:
                    if j in prop_lst:
                        temp.append(j)
                dct['claims'] = temp
                item_dct.append(dct)
            except:
                invalid_item = invalid_item + 1
        if entity_dict['type']=='property':
            try:
                dct['_key'] = entity_dict['id']
                dct['type'] = entity_dict['type']
                dct['label'] = entity_dict['labels']['en']['value']
                dct['description'] = entity_dict['descriptions']['en']['value']
#                 dct['label'] = entity_dict['labels']
#                 dct['description'] = entity_dict['descriptions']
                prop_dct.append(dct)

            except:
                invalid_prop = invalid_prop + 1

# CREATING AND CONNECTING TO DATABASE AND COLLECTIONS
conn = CON.Connection(username=USERNAME,password=PASSWORD)
if conn.hasDatabase(DB_NAME):
    print('Database already present')
    db = conn.databases[DB_NAME]
else:
    conn.createDatabase(DB_NAME)
    db = conn.databases[DB_NAME]
    print('Database created')
if db.hasCollection(ITEM_COLLECTION):
    print('Collection already exists')
    t2_item = db.collections[ITEM_COLLECTION]
else:
    t2_item = db.createCollection("Collection",name=ITEM_COLLECTION)
    print('New Item Collection Created')
    
if db.hasCollection(PROP_COLLECTION):
    print('Collection already exists')
    t2_prop = db.collections[PROP_COLLECTION]
else:
    t2_prop = db.createCollection("Collection",name=PROP_COLLECTION)
    print('New Property Collection Created')
    
if db.hasCollection(EDGE_COLLECTION):
    print('Edge collection already exists')
    t2_edge = db.collections[EDGE_COLLECTION]
else:
    t2_edge = db.createCollection("Edges",name=EDGE_COLLECTION)
    print('New Edge Collection created.')
    
# SAVING ITEM COLLECTION DOCUMENTS
for i in item_dct:
    doc = t2_item.createDocument()
    for j in i.keys():
        doc[j] = i[j]
    doc.save()

# SAVING PROPERTY COLLECTION DOCUMENTS
for i in prop_dct:
    doc = t2_prop.createDocument()
    for j in i.keys():
        doc[j] = i[j]
    doc.save()

# SAVING EDGES
for i in item_dct:
    for j in i['claims']:
        if j in prop_lst:
            doc = t2_edge.createEdge()
            doc['_from'] = f"{ITEM_COLLECTION}/{i['_key']}"
            doc['_to'] = f"{PROP_COLLECTION}/{j}"
            doc['prop'] = t2_prop.fetchDocument(j,rawResults=True)['label']
            doc.save()
 
# CREATING GRAPH
class final_edge(Edges):
    pass
class final_item(Collection):
    pass
class final_prop(Collection):
    pass
edge_definition = EdgeDefinition('final_edge', fromCollections=['final_item'], toCollections=['final_prop'])
class final_graph(Graph) :
    _edgeDefinitions = [edge_definition]
    _orphanedCollections = []
db.createGraph(name="final_graph", createCollections=True)
print("Graph Created Successfully!")