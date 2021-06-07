# Read Ontology

The most basic thing we need to do is read files.

## Results

Tool | Exit status | Maximum resident set size (kbytes) | User time (seconds) | Percent of CPU this job got
--- | --: | --: | --: | --:
[horned-owl](https://github.com/phillord/horned-owl) | 0 | 8448 | 0.00 | 76%
[py-horned-owl](https://github.com/jannahastings/py-horned-owl) | 0 | 15456 | 0.03 | 81%
[rdftab-thick](https://github.com/ontodev/rdftab.rs) | 127 | 1700 | 0.00 | 0%
[rdftab-thin](https://github.com/ontodev/rdftab.rs) | 0 | 4124 | 0.02 | 28%
[robot](http://robot.obolibrary.org) | 0 | 126504 | 2.32 | 236%

## Tools

### robot

`robot annotate` does more than just read,
but not *much* more.

```sh
robot annotate --input /work/example/obi_core.owl --ontology-iri "httpL//example.com"
```

### horned-owl

horned-owl 0.9.0 has some support for reading RDFXML,
but here we read OWLXML.

```sh
horned-parse /work/example/obi_core.owx
```

### py-horned-owl

py-horned-owl 0.1.4 can only read and write OWLXML.

```py
import pyhornedowl

onto = pyhornedowl.open_ontology("/work/example/obi_core.owx")
```

```sh
python test.py
```

### rdftab-thin

RDFTab 0.1.1 supports "thin triples".

```sh
sqlite3 obi_core.db < /work/example/obi_core_prefixes.sql
rdftab-thin obi_core.db < /work/example/obi_core.owl
```

### rdftab-thick

TODO

