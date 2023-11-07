import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def calculate_continent_areas():
    g = rdflib.Graph()

    g.parse("countrues_info.ttl", format="ttl")

    query = """
    PREFIX ex: <http://example.com/demo/>
    SELECT ?contName (SUM(?area) AS ?total_area)
    WHERE {
        ?country a ex:Country ;
        ex:part_of_continent ?continent;
        ex:area_in_sq_km ?area .
        ?continent a ex:Continent;
        ex:continent_name ?contName .
    }
    GROUP BY ?continent
    ORDER BY DESC(?total_area)
    """

    results = g.query(query)
    print("Here's the results:\n")
    for row in results:
        print(str(row["contName"])+" "+str(round(float(row["total_area"]))))


def get_biggest_city():
    g = rdflib.Graph()
    query = """PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?cityName ?population
WHERE {
  ?city a dbo:City ;
        dbo:country <http://dbpedia.org/resource/Ukraine> ;
        dbo:populationTotal ?population ;
        rdfs:label ?cityName .
  FILTER (LANGMATCHES(LANG(?cityName), 'en'))
}
ORDER BY DESC(?population)
LIMIT 1"""
    print("Here's the SPARQL query:")
    print("===============")
    print(query)
    print("===============")
    print("Here's the results:\n")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print(result["cityName"]["value"] + " - " + result["population"]["value"])

def get_eng_countries():
    g = rdflib.Graph()
    #У якості "фільтру" було використано countryCode - так як просто пошук за типом
    #dbo:Country повертав дуже багато організацій, міжнародних угод і тд,
    #а окремий список лише усіх країн знайти не вдалося
    query = """PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?countryName ?population
WHERE {
  ?country a dbo:Country ;
           dbo:language <http://dbpedia.org/resource/English_language> ;
           rdfs:label ?countryName ;
           dbo:populationTotal ?population ;
           dbo:countryCode ?countryCode .
  FILTER (LANGMATCHES(LANG(?countryName), 'en'))
  FILTER (BOUND(?countryCode))
}
ORDER BY DESC(?population)"""

    print("Here's the results:\n")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print(result["countryName"]["value"] + " - " + result["population"]["value"])

while (True):
    print("\n===============")
    print("Select task 1, 2 or 3\nEnter 0 to exit")
    print("===============\n")
    menu = input()
    if menu == "1":
        calculate_continent_areas()
    elif menu == "2":
        get_biggest_city()
    elif menu == "3":
        get_eng_countries()
    else:
        break


