# tooling-comparison

Docs and tests comparing RDF and OWL tooling.

## Results

Task | [horned-owl](https://github.com/phillord/horned-owl) | [py-horned-owl](https://github.com/jannahastings/py-horned-owl) | [rapper](https://librdf.org/raptor/) | [rdftab-thick](https://github.com/ontodev/rdftab.rs) | [rdftab-thin](https://github.com/ontodev/rdftab.rs) | [robot](http://robot.obolibrary.org)
--- | --- | --- | --- | --- | --- | ---
[convert-ontology](task/convert-ontology.md) |  |  | FAIL | FAIL | FAIL | PASS

## Tools

These are relevant tools that we will consider testing:

- [ROBOT](http://robot.obolibrary.org)
- [horned-owl](https://github.com/phillord/horned-owl)
- [RDFTab](https://github.com/ontodev/rdftab.rs) thin triples
  - [semantic-sql](https://github.com/cmungall/semantic-sql)
  - [Gizmos](https://github.com/ontodev/gizmos)
- RDFTab thick triples
- [Raptor](https://librdf.org/raptor/)
- [Apache Jena](https://jena.apache.org)
- [funowl](https://github.com/hsolbrig/funowl)
- [owlready2](https://github.com/pwin/owlready2)

## Tasks

These are some relevant tasks we will consider including:

- read ontology: e.g. `robot annotate`
- convert ontology: e.g. `robot convert`
- extract labels: e.g. `robot export`
- extract term: e.g. `robot extract`
- get subclasses of a term:
- get interesting axioms from a term:
- update label: e.g. `robot rename`
- update axiom: 


## Run

The various tools are packaged in a Docker container
that builds on [odkfull](https://hub.docker.com/r/obolibrary/odkfull).
Docker is the only requirement,
usually installed with
[Docker Desktop](https://www.docker.com/products/docker-desktop)

First you need to build the Docker image:

```sh
docker build --tag ontodev-tooling-comparison .
```

Then you run the tests with:

```sh
docker run --rm -v $(pwd):/work -w /work ontodev-tooling-comparison
```

See the `result/` directory for detailed results.

## Design

Each task is described in a Markdown file.
For each task we create a `result/task/` directory.
For each tool we create a `result/task/tool/` subdirectory.

Each task Markdown file includes a "Tools" section
with subsections for each specific tool.
Each subsection (when complete)
contains a code block that defines a script
for running that task with that specific tool.
This code block will be used to generate a
`result/task/tool/test.sh` script.

For each task and each tool
we first generate the subdirectory and `test.sh` script
then run `/usr/bin/time -v sh test.sh > result.txt`
in the subdirectory.
The various result.txt files can be used to compare performance.

For each task we generate a `result/task/summary.tsv` table.
We also generate PASS/FAIL summary in `result/summary.tsv`.

Before running tasks we write some system information
to `result/system.txt`.
