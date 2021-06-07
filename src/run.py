#!/usr/bin/env python3

import csv
import os
import shutil
import subprocess

from collections import defaultdict

TASK_DIR = "task/"
RESULT_DIR = "result/"
SUMMARY_FIELDS = [
  "Tool",
  "Exit status",
  "Maximum resident set size (kbytes)",
  "User time (seconds)",
  "Percent of CPU this job got",
]
links = {
    "robot": "http://robot.obolibrary.org",
    "horned-owl": "https://github.com/phillord/horned-owl",
    "py-horned-owl": "https://github.com/jannahastings/py-horned-owl",
    "rdftab-thin": "https://github.com/ontodev/rdftab.rs",
    "rdftab-thick": "https://github.com/ontodev/rdftab.rs",
    "rapper": "https://librdf.org/raptor/",
}


def update_results(document, table):
    """Given paths to a document and a table,
    both in Markdown format,
    replace the '## Results' section of the document
    with the lines from the table."""
    print("Updating", document)
    with open(document) as f:
        document_lines = list(f.readlines())
    with open(table) as f:
        table_lines = list(f.readlines())
    results_section = False
    output_lines = []
    for line in document_lines:
        if line.strip() == "## Results":
            results_section = True
            output_lines += [line, "\n"] + table_lines + ["\n"]
            continue
        if line.strip().startswith("#"):
            results_section = False
        if results_section:
            continue
        else:
            output_lines.append(line)
    with open(document, "w") as f:
        f.write("".join(output_lines))


def run_task(task):
    """Given a task name,
    read the Markdown file,
    generate subdirectories and scripts,
    then run all the scripts."""
    fname = os.path.join(TASK_DIR, task + ".md")
    tools = None
    tool = None
    filename = None
    script = False
    with open(fname) as f:
        for line in f.readlines():
            if line.strip() == "## Tools":
                tools = {}
                continue
            if tools == None:
                continue
            if line.strip().startswith("## "):
                break
            if line.strip().startswith("### "):
                tool = line.strip().lstrip("#").strip()
                if tool in tools:
                    raise Exception(f"Duplicate tool specified: '{tool}'")
                tools[tool] = defaultdict(list)
                continue
            if line.strip() == "```":
                script = False
                continue
            if line.strip().startswith("```"):
                script = True
                format = line.strip().lstrip("`")
                filename = f"test.{format}"
                continue
            if tool and script:
                tools[tool][filename].append(line)

    results = {}
    for tool, scripts in tools.items():
        results[tool] = {"Tool": tool}
        path = os.path.join(RESULT_DIR, task, tool)
        os.makedirs(path, exist_ok=True)
        for filename, lines in scripts.items():
            if not lines:
                continue
            script = os.path.join(path, filename)
            with open(script, "w") as f:
                f.write("\n".join(lines))
        result = os.path.join(path, "result.txt")
        print("Running", script)
        with open(result, "w") as f:
            subprocess.run(
              ["/usr/bin/time", "-v", "sh", "test.sh"],
              cwd=path,
              stdout=f,
              stderr=subprocess.STDOUT
            )
        with open(result) as f:
            reading = False
            for line in f.readlines():
                if line.strip() == "Command being timed: \"sh test.sh\"":
                    reading = True
                    continue
                if not reading:
                    continue
                key, value = line.strip().split(": ", 1)
                results[tool][key] = value

    summary = os.path.join(RESULT_DIR, task, "summary.tsv")
    print("Writing", summary)
    with open(summary, "w") as f:
        writer = csv.DictWriter(
          f,
          SUMMARY_FIELDS,
          extrasaction="ignore",
          delimiter="\t",
          lineterminator="\n"
        )
        writer.writeheader()
        tools = sorted(list(results.keys()))
        for tool in tools:
            writer.writerow(results[tool])

    summary_md = os.path.join(RESULT_DIR, task, "summary.md")
    print("Writing", summary_md)
    with open(summary) as f:
        rows = csv.reader(f, delimiter="\t")
        with open(summary_md, "w") as s:
            row = next(rows)
            s.write(" | ".join(row) + "\n")
            header = ["---"] + ["--:" for r in row[1:]]
            s.write(" | ".join(header) + "\n")
            for row in rows:
                tool = row[0]
                if tool in links:
                    row[0] = f"[{tool}]({links[tool]})"
                s.write(" | ".join(row) + "\n")

    update_results(fname, summary_md)

    return results


def run():
    shutil.rmtree(RESULT_DIR)
    os.makedirs(RESULT_DIR)

    system = os.path.join(RESULT_DIR, "system.txt")
    with open(system, "w") as f:
        subprocess.run(
          ["lscpu"],
          stdout=f,
          stderr=subprocess.STDOUT
        )
        subprocess.run(
          ["free"],
          stdout=f,
          stderr=subprocess.STDOUT
        )

    results = {}
    for f in os.listdir(TASK_DIR):
        if not f.endswith(".md"):
            continue
        task, ext = os.path.splitext(f)
        results[task] = run_task(task)

    all_tools = set()
    for task, tools in results.items():
        all_tools.update(set(list(tools.keys())))
    all_tools = list(all_tools)
    all_tools.sort()

    summary = os.path.join(RESULT_DIR, "summary.tsv")
    print("Writing", summary)
    with open(summary, "w") as f:
        writer = csv.DictWriter(
          f,
          ["Task"] + all_tools,
          extrasaction="ignore",
          delimiter="\t",
          lineterminator="\n"
        )
        writer.writeheader()
        for task, tools in results.items():
            row = {"Task": task}
            for tool in all_tools:
                if tool not in tools:
                    row[tool] = ""
                elif "Exit status" not in tools[tool]:
                    row[tool] = ""
                elif tools[tool]["Exit status"] == "0":
                    row[tool] = "PASS"
                else:
                    row[tool] = "FAIL"
            writer.writerow(row)

    summary_md = os.path.join(RESULT_DIR, "summary.md")
    print("Writing", summary_md)
    with open(summary) as f:
        rows = csv.reader(f, delimiter="\t")
        with open(summary_md, "w") as s:
            row = next(rows)
            for i in range(1, len(row)):
                tool = row[i]
                if tool in links:
                    row[i] = f"[{tool}]({links[tool]})"
            s.write(" | ".join(row) + "\n")
            s.write(" | ".join("---" for r in row) + "\n")
            for row in rows:
                row[0] = f"[{row[0]}](task/{row[0]}.md)"
                s.write(" | ".join(row) + "\n")

    update_results("README.md", summary_md)

if __name__ == "__main__":
    run()

