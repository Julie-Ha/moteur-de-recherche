

-----------------------------
Information about the files
-----------------------------



article_typeid.json   ---->   This file contains the types(type-id) associated with each of the articles.

article_vector.json   ---->   This file contains the type vector for each of the articles.

dimension_name.txt    ---->    This file contains the name of the dimension of the vectors present in article_vector.json.

typeid_name_wordnet.json    ---->    This file contains information about each of the types.

"container.self-propelled_vehicle": {"name": "self-propelled_vehicle", "type": "<wordnet_self-propelled_vehicle_104170037>"}
Here key value is "type-id" ("container.self-propelled_vehicle"). Values are name of the type ("name": "self-propelled_vehicle") and wordnet form of that type ("type": "<wordnet_self-propelled_vehicle_104170037>")

ontology.csv    ----->    This file contains child, parent pair in each line. Root node is entity.


--> 	typeid_name_wordnet.json -> entités et liens entre elles

	article_typeid.json -> avant de vectoriser
	article_vector.json -> calcule cosine_similarity en python avec sklearn
--> ontology.csv -> afficher les entités en arbre 