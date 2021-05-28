#!/usr/bin/env python3

TASK_DIR = "tasks/"

def run_task(name):
    fname = os.path.join(TASK_DIR, name)
    tools = False
    tool = None
    script = False
    output = {}
    with open(fname) as f:
        for line in f.readlines():
            if line.strip() == "## Tools":
                tools = True
                continue
            if not tools:
                continue
            if line.strip().startswith("## "):
                break
            if line.strip().startswith("### "):
                tool = line.strip().lstrip("#").strip()
                if tool in output:
                    raise Exception(f"Duplicate tool specified: '{tool}'")
                output[tool] = []
                continue
            if line.strip().startswith("```sh"):
                script = True
                continue
            if line.strip().startswith("```"):
                script = False
                continue
            if tool and script:
                output[tool].append(line)
    print(output)


def run():
    for f in os.listdir(TASK_DIR):
        if not f.endswith(".md"):
            continue
        run_task(f)


if __name__ == "__main__":
    run()

