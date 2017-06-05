# BAMPFA Exhibition History

## About

This is a first stab at gathering additional information on BAMPFA exhibition history for eventual display on [bampfa.org](http://bampfa.org). So far this is just a script to get ULAN info for artists featured in past exhibitions. The Getty Research Institute's ULAN vocabulary is a controlled list of artist names that is available as [Linked Open Data](http://vocab.getty.edu/). 


## sparqlGetty

This script takes a csv list of names formatted "LastName, FirstName" and for each result returns the following:


|Getty URI|Artist Name|ULAN Bio|ULAN Scope Note|Also Known As|Type of Artist|
|-|-|-|-|-|-|
http://vocab.getty.edu/ulan/500009666|"Picasso, Pablo"|Spanish painter, sculptor, and printmaker, 1881-1973|Long-lived and very influential Spanish artist, active in France. He dominated 20th-century European art. With Georges Braque, he is credited with inventing Cubism.|Pablo Picasso;Picasso, Pablo Diego José Francisco de Paula Juan Nepomuceno Crispín Crispiniano de la Santissima Trinidad Ruiz Blasco;Picasso, Pablo Ruiz;Picasso, Pablo Ruiz y;Ruiz Picasso, Pablo;Ruiz y Picasso, Pablo;Ruiz, Pablo;Ruys Picasso, Pablo;Ruys, Pablo;Ruiz Y Picasso, Pablo;Picasso, Pablo Ruiz Y;Pablo Ruiz Y Picasso|ceramicists;artists;decorative artists;genre artists;painters;sculptors|

It borrows from [SFMoMA's](https://github.com/sfmoma/getty-getter) efforts along the same lines and uses plain text (UTF-8!) names to query the ULAN [SPARQL](https://data-gov.tw.rpi.edu/wiki/How_to_use_SPARQL) endpoint. I found [Getty's query interface](http://vocab.getty.edu/queries#Finding_Subjects) more or less helpful in exploring the ULAN and other relevant ontologies... 

#### Usage

The data going in should be as clean as possible so I used a combination of [OpenRefine](http://openrefine.org/) and a text editor to get unique values, swap FirstName/LastName and so on. If the input csv isn't properly quoting each row then each name will fail.

`cd` into the directory where you put the script. You'll want to change the relative paths of the input and output files (i.e., not '*/samples/in.csv'). `python sparqlGetty.py` and see what comes out. 

Note that any non-disambiguated (undisambiguated? ambiguated?) names return multiple rows in the output csv, so it requires someone going through and figuring out which `Picasso, Pablo` you are talking about. Also, non-matches are ignored and there is no guarantee that a result is the one you are looking for (i.e. there could be a result for `Newman, Alfred E.`, but maybe the ULAN listed person is not the one you are looking for).

#### Dependencies

[SPARQLWRAPPER](https://rdflib.github.io/sparqlwrapper/)

#### Rights

This project contains information from Union List of Artist Names (ULAN)® which is made available under the ODC Attribution License.
