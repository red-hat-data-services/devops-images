#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jinja2", "pyyaml"]
# ///
"""Generate Tekton PipelineRun YAML files from Jinja2 templates."""

import os

import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEKTON_DIR = os.path.join(REPO_ROOT, ".tekton")
TEKTON_TEMPLATES_DIR = os.path.join(TEKTON_DIR, "templates")
CONFIG_FILE = os.path.join(REPO_ROOT, "components.yaml")

TEMPLATES = [
    ("pull-request.yaml.j2", "pull-request"),
    ("push.yaml.j2", "push"),
]


def main():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)

    env = Environment(
        loader=FileSystemLoader(TEKTON_TEMPLATES_DIR),
        keep_trailing_newline=True,
    )

    for tmpl_file, suffix in TEMPLATES:
        template = env.get_template(tmpl_file)
        for comp in config["components"]:
            context = {
                "component_name": comp["name"],
                "image_name": comp["image_name"],
                "path_context": comp["context"],
                "git_url": config["git_url"],
                "image_prefix": config["image_prefix"],
            }
            if comp.get("additional_secret"):
                context["additional_secret"] = comp["additional_secret"]
            out_name = f"{comp['name']}-{suffix}.yaml"
            out_path = os.path.join(TEKTON_DIR, out_name)
            rendered = template.render(**context)
            with open(out_path, "w") as f:
                f.write(rendered)
            print(f"Generated {out_name}")


if __name__ == "__main__":
    main()
