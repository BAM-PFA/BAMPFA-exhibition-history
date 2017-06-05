#!/usr/bin/env python

import json, os, csv
from SPARQLWrapper import SPARQLWrapper, JSON

null = ""
currentDirectory = os.getcwd()

ULANuri = ["Getty URI"]
artistName = ["Artist Name"]
ULANbio = ["ULAN Bio"]
ULANscopeNote = ["ULAN Scope Note"]
akas = ["Also Known As"]
roles = ["Type of Artist"]

with open(currentDirectory+"/samples/exhibitionPersons.csv","r+") as artistFile:
    # Make sure that the csv format provides quoted names or it will all fail.
    # In this list, artists are entered "Lastname, Firstname"
    # Also could make a function to get results by ULAN id, which is way simpler
    artistList = []
    for line in artistFile:
        artist = line.rstrip('\n').replace("'","\\\'")
        artistList.append(artist)

for artist in artistList:
    # To do: get the singular form of each role. ie, painter not painters. preferred gvp term is plural.
    # Hunt for the singular value that feeds the Getty website view?
    queryString ='''
PREFIX  gvp:  <http://vocab.getty.edu/ontology#>
PREFIX  schema: <http://schema.org/>
PREFIX  ulan: <http://vocab.getty.edu/ulan/>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX  skosx: <http://www.w3.org/2008/05/skos-xl#>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>

SELECT  ?labelURI ?bio ?scopeNote (GROUP_CONCAT(DISTINCT ?aka ; separator='|') AS ?akas) (GROUP_CONCAT(DISTINCT ?role ; separator='|') AS ?roles)
WHERE
  { ?labelURI  rdfs:label  '''+artist+''';
    (foaf:focus/gvp:biographyPreferred)/schema:description ?bio
    OPTIONAL
      { ?labelURI skos:scopeNote/rdf:value ?scopeNote }
    OPTIONAL
      { ?labelURI skosx:altLabel/gvp:term ?aka }
    OPTIONAL
      { ?labelURI gvp:agentType/skosx:prefLabel/gvp:term ?role
        FILTER ( lang(?role) = "en" )
      }
  }
GROUP BY ?labelURI ?bio ?scopeNote
'''
    sparql = SPARQLWrapper("http://vocab.getty.edu/sparql")
    sparql.setQuery(queryString)
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        bindings = results['results']['bindings']

        for result in bindings:
            # Ignore null results. Get a "first key" for the dict that is returned and check it for contents.
            # To do: currently all results are returned, and there's no flag for multiple results. 
            # Either the names should be pre-checked/verified as unique or there should be a filter
            # to get rid of extraneous results.
            # print(result)
            firstKey = next(iter(result))
            if result[firstKey]['value'] != null:
                if 'labelURI' in result:
                    result_uri = result['labelURI']['value']
                else:
                    result_uri = null
                if 'akas' in result:
                    result_akas = result['akas']['value']
                else:
                    result_akas = null
                if 'scopeNote' in result:
                    result_scopeNote = result['scopeNote']['value']
                else:
                    result_scopeNote = null
                if 'bio' in result:
                    result_bio = result['bio']['value']
                else:
                    result_bio = null
                if 'roles' in result:
                    result_roles = result['roles']['value']
                else:
                    result_roles = null
                ULANuri.append(result_uri)
                artistName.append(artist)
                ULANbio.append(result_bio)
                ULANscopeNote.append(result_scopeNote)
                akas.append(result_akas)
                roles.append(result_roles)
                print(result_uri)
                print(result_akas)
                print(result_scopeNote)
                print(result_bio)
                print(result_roles)

    except:
        results = "Failed on: "
        print(results+artist)

outputRows = zip(ULANuri,artistName,ULANbio,ULANscopeNote,akas,roles)
with open(currentDirectory+"/samples/ULANoutput.csv", "w+") as output:
    writer = csv.writer(output)
    for row in outputRows:
        writer.writerow(row)