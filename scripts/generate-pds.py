#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jinja2", "pyyaml"]
# ///
"""Generate Konflux ProjectDevelopmentStream YAML from Jinja2 template."""

import os

import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")
KONFLUX_DIR = os.path.join(REPO_ROOT, ".konflux")
CONFIG_FILE = os.path.join(REPO_ROOT, "config.yaml")


def main():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)

    os.makedirs(KONFLUX_DIR, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        keep_trailing_newline=True,
    )

    template = env.get_template("pds.yaml.j2")
    rendered = template.render(**config)
    out_path = os.path.join(KONFLUX_DIR, "ProjectDevelopmentStream.yaml")
    with open(out_path, "w") as f:
        f.write(rendered)
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
