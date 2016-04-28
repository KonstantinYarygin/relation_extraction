from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dbp: <http://dbpedia.org/property/>

# from all the stuff below give me ?name and ?type
SELECT DISTINCT ?name, ?type WHERE {

# it means: get all food (?food) which has ingredient (?ing_link)
?food dbo:ingredient ?ing_link .

# from ingredient (?ing_link) get property rdfs:label (?name )
?ing_link rdfs:label ?name .

# if ingredient ?ing_link has any types, include it all (?type)
OPTIONAL { ?ing_link rdf:type ?type . }

# get only english ?name
FILTER langMatches(lang(?name),'en')
}
ORDER BY ?name
"""
sparql.setReturnFormat(JSON)

empty = False
limit = 10000
offset = 0
offset_step = limit

output_file = "food.csv"
f = open(output_file, 'w')

while not empty:
    print("offset is %i" % offset)
    sparql.setQuery(query + "\nLIMIT %i OFFSET %i" % (limit, offset))
    results = sparql.query().convert()
    results_list = results["results"]["bindings"]
    if len(results_list) == 0:
        empty = True
        break
    for result in results_list:
        food_name = result["name"]["value"]
        food_type = ""
        try:
            food_type = result["type"]["value"]
        except:
            pass
        row = "%s\t%s\n" % (food_name, food_type)
        f.write(row)
    offset += offset_step

f.close()
