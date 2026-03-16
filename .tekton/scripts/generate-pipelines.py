#!/usr/bin/env python3
"""Generate Tekton PipelineRun YAML files from Jinja2 templates."""

import os
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEKTON_DIR = os.path.dirname(SCRIPT_DIR)
TEMPLATES_DIR = os.path.join(TEKTON_DIR, "templates")

COMPONENTS = [
    {
        "component_name": "devops-base-runner",
        "image_name": "base-runner",
        "path_context": "base",
    },
    {
        "component_name": "devops-openshift-utils",
        "image_name": "openshift-utils",
        "path_context": "openshift-utils",
    },
    {
        "component_name": "devops-tracer",
        "image_name": "tracer",
        "path_context": "tracer",
        "additional_secret": "devops-infra-ssh-key-devops-image-builds",
    },
]

TEMPLATES = [
    ("pull-request.yaml.j2", "pull-request"),
    ("push.yaml.j2", "push"),
]


def main():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        keep_trailing_newline=True,
    )

    for tmpl_file, suffix in TEMPLATES:
        template = env.get_template(tmpl_file)
        for comp in COMPONENTS:
            out_name = f"{comp['component_name']}-{suffix}.yaml"
            out_path = os.path.join(TEKTON_DIR, out_name)
            rendered = template.render(**comp)
            with open(out_path, "w") as f:
                f.write(rendered)
            print(f"Generated {out_name}")


if __name__ == "__main__":
    main()
