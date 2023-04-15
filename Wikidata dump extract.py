
import qwikidata
from qwikidata.entity import WikidataItem, WikidataProperty
import pyArango.connection as CON
path = 'D:\\wikidata-v1\\v1.json.gz'


from qwikidata.json_dump import WikidataJsonDump

wjd = WikidataJsonDump(path)

type_to_entity_class = {"item": WikidataItem, "property": WikidataProperty}
max_entities = 200
print(type_to_entity_class)
entities = []


for ii, entity_dict in enumerate(wjd):
    if ii >= max_entities:
        break
    entity_id = entity_dict["id"]
    entity_type = entity_dict["type"]
    if entity_type=="item":
        entities.append(entity_dict)
#     if(entity_type=='property'):
# #         print(entity_dict.keys())
#         entity_dict['claims']=' '
#         entity = WikidataProperty(entity_dict)
#         print(entity)
#     print(f"---------------{ii}--------------------")
#     print(entity_type)
#     entity = type_to_entity_class[entity_type](entity_dict)
#     entities.append(entity_type)

# for entity in entities:
#     print(entity)

db = CON.Connection(username="root",password="").databases["test1"]

dd = db.collections["wikidata-v1"]

for i in entities:
    doc = dd.createDocument()
    for j in i.keys():
        doc[j] = i[j]
    doc.save()


