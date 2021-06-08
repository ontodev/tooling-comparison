# Extract Labels

A common task is extracting a set of IDs and labels from an ontology.

## Results

Tool | Exit status | Maximum resident set size (kbytes) | User time (seconds) | Percent of CPU this job got
--- | --: | --: | --: | --:
[horned-owl](https://github.com/phillord/horned-owl) | 1 | 13824 | 0.01 | 76%
[py-horned-owl](https://github.com/jannahastings/py-horned-owl) | 0 | 15768 | 0.03 | 79%
[rapper](https://librdf.org/raptor/) | 0 | 11280 | 0.01 | 93%
[rdftab-thick](https://github.com/ontodev/rdftab.rs) | 127 | 1588 | 0.00 | 0%
[rdftab-thin](https://github.com/ontodev/rdftab.rs) | 0 | 4288 | 0.00 | 18%
[robot](http://robot.obolibrary.org) | 0 | 141448 | 2.21 | 242%

## Tools

### robot

```sh
robot export --input /work/example/obi_core.owl \
  --header "ID|LABEL" \
  --export obi_core.tsv
```

### horned-owl

We read OWLXML,
stream to triples,
then grep and format them.

```sh
horned-triples /work/example/obi_core.owx \
| grep " <http://www.w3.org/2000/01/rdf-schema#label> " \
| cut -d " " -f 1,3 \
> obi_core.tsv
test -s obi_core.tsv
```

### py-horned-owl

We read OWLXML and then extract IRIs and labels.

```py
import pyhornedowl
import csv

onto = pyhornedowl.open_ontology('/work/example/obi_core.owx')
with open("obi_core.tsv", "w") as f:
  w = csv.writer(f, delimiter="\t", lineterminator="\n")
  w.writerow(["IRI", "Label"])
  for cls in onto.get_classes():
      label = onto.get_annotation(cls, "http://www.w3.org/2000/01/rdf-schema#label")
      w.writerow([cls, label])
```

```sh
python test.py
```

### rdftab-thin

An advantage of RDFTab is that you can reuse a parsed ontology,
rather than reading it again every time.
Here we use an existing SQLite database,
and use SQL to extract IDs and labels.

```sql
.headers on
.mode tabs
SELECT subject as "ID", value as "Label"
FROM statements
WHERE predicate = "rdfs:label";
```

```sh
sqlite3 /work/example/obi_core_rdftab-thin.db < test.sql > obi_core.tsv
```

### rdftab-thick

TODO

### rapper

We stream to N-Triples then `grep`.

```sh
rapper /work/example/obi_core.owl \
| grep " <http://www.w3.org/2000/01/rdf-schema#label> " \
| cut -d " " -f 1,3 \
> obi_core.tsv
test -s obi_core.tsv
```

