import os
import time

from SPARQLWrapper import SPARQLWrapper, JSON

# you can check the query as it is at: http://dbpedia.org/sparql
#
# here is online editor: http://sparql.carsten.io/
#

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
script_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(script_dir, "get_food.sparql"), 'r') as content_file:
    query = content_file.read()
sparql.setReturnFormat(JSON)

empty = False
limit = 10000
offset = 0
offset_step = limit

output_file = "food.csv"
f = open(output_file, 'w')
header = "name\ttypelink\ttype\tsubjectlink\tsubject"
rows = []
while not empty:
    print("offset is %i" % offset)
    start = time.time()
    sparql.setQuery(query + "\nLIMIT %i OFFSET %i" % (limit, offset))
    results = sparql.query().convert()
    end = time.time()
    print("got result in %f seconds" % (end - start))
    results_list = results["results"]["bindings"]
    if len(results_list) == 0:
        empty = True
        break
    for result in results_list:
        food_name = result["name"]["value"]
        food_type = ""
        food_type_name = ""
        food_subject = ""
        food_subject_name = ""
        try:
            food_type = result["type"]["value"]
            food_type_name = result["typename"]["value"]
        except:
            pass
        try:
            food_subject = result["subject"]["value"]
            food_subject_name = result["subjectname"]["value"]
        except:
            pass
        row = "%s\t%s\t%s\t%s\t%s\n" % (food_name, food_type, food_type_name, food_subject, food_subject_name)
        f.write(row)

    offset += offset_step

f.close()
