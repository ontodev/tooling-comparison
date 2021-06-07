# Convert Ontology

A common task is converting from one format to another.
This tests the tool's read and write performance.

OWLAPI supports the widest range of formats,
but there are other tools such as `rapper` and `riot`
that can easily convert between formats.

format | ROBOT | horned-owl | RDFTab
-------|-------|------------|-------
Turtle | X     |            | X
RDFXML | X     | X          |
OWLXML | X     | X          |
OBO    | X     |            |
OFN    | X     |            |
OMN    | X     |            |

## Results

Tool | Exit status | Maximum resident set size (kbytes) | User time (seconds) | Percent of CPU this job got
--- | --: | --: | --: | --:
[horned-owl](https://github.com/phillord/horned-owl) | 0 | 7760 | 0.07 | 9%
[py-horned-owl](https://github.com/jannahastings/py-horned-owl) | 0 | 15668 | 0.13 | 8%
[rapper](https://librdf.org/raptor/) | 0 | 11328 | 0.01 | 37%
[rdftab-thick](https://github.com/ontodev/rdftab.rs) | 127 | 1696 | 0.00 | 0%
[rdftab-thin](https://github.com/ontodev/rdftab.rs) | 0 | 5588 | 0.02 | 31%
[robot](http://robot.obolibrary.org) | 0 | 144380 | 3.02 | 183%

## Tools

### robot

```sh
robot convert --input /work/example/obi_core.owl --output obi_core.ttl
```

### horned-owl

horned-owl 0.9.0 has some support for reading RDFXML,
but here we just read then write OWLXML.
This is very fast,
but for some reason the process stays open for about 9 seconds,
making it seem slow to the user.

```sh
horned-round /work/example/obi_core.owx > obi_core.owx
```

### py-horned-owl

py-horned-owl 0.1.4 can only read and write OWLXML.
Like horned-owl, there is a delay closing the file,
which means the wall-clock time is slow.

```py
import pyhornedowl

onto = pyhornedowl.open_ontology("/work/example/obi_core.owx")
onto.save_to_file("obi_core.owx")
```

```sh
python test.py
```

### rdftab-thin

RDFTab 0.1.1 supports "thin triples"
and has fairly crude output to Turtle format.

```sh
sqlite3 obi_core.db < /work/example/obi_core_prefixes.sql
rdftab-thin obi_core.db < /work/example/obi_core.owl
sqlite3 obi_core.db < /work/example/rdftab-thin_turtle.sql > obi_core.ttl
```

### rdftab-thick

TODO

### rapper

`rapper` supports a number of RDF formats
for input and output.
The default output format is N-Triples.

```sh
rapper /work/example/obi_core.owl > obi_core.nt
```

