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

## Harness

We use ROBOT to check that the output matches the input.

```sh
time -v sh task.sh > results.txt
robot diff --left /work/example/obi_core.owl --right obi_core.ttl --output obi_core.diff
```

## Tools

### robot

```sh
robot convert --input /work/example/obi_core.owl --output obi_core.ttl
```

### horned-owl

TODO

### py-horned-owl

TODO

### rdftab-thin

```sh
sqlite3 obi_core.db < /work/example/obi_core-prefixes.sql
rdftab-thin obi_core.db < /work/example/obi_core.owl
sqlite3 obi_core.db < /work/tools/rdftab-thin/turtle.sql > obi_core.ttl
```

### rdftab-thick

Note that thick triples to Turtle is currently in Python.

```sh
sqlite3 obi_core.db < /work/example/obi_core-prefixes.sql
rdftab-thick obi_core.db < /work/example/obi_core.owl
sqlite3 obi_core.db < /work/tools/rdftab-thick/turtle.sql > obi_core.ttl
```

### rapper

```sh
rapper /work/example/obi_core.owl > obi_core.ttl
```

