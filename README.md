# DevOps Images

Container image factory for RHOAI DevOps. Builds and publishes pre-built runner images to `quay.io/rhoai-devops` so that CI/CD tasks can use them directly without installing tools at runtime.

All images build for **linux/x86_64** and **linux/arm64**.

## Images

```
base-runner
├── openshift-utils
└── tracer
```

| Image | Directory | Base | Tools |
|-------|-----------|------|-------|
| base-runner | `builds/base/` | UBI 9 | yq, skopeo, podman, git, jq, gettext |
| openshift-utils | `builds/openshift-utils/` | base-runner | oc, kubectl, opm |
| tracer | `builds/tracer/` | base-runner | tracer.sh (from private rhods-devops-infra repo) |

## How it works

Everything is driven by `config.yaml` at the repo root. Two generation scripts read it and produce config from Jinja2 templates:

- **`scripts/generate-pipelines.py`** — Tekton PipelineRun YAMLs in `.tekton/`
- **`scripts/generate-pds.py`** — Konflux ProjectDevelopmentStream YAML in `.konflux/`

```bash
uv run scripts/generate-pipelines.py
uv run scripts/generate-pds.py
```

Dependencies (`jinja2`, `pyyaml`) are declared inline via PEP 723 — `uv` handles them automatically.

### argfile.conf (per-image)

Each image directory under `builds/` has its own `argfile.conf` with pinned SHA256 digests for reproducible builds. Renovate automatically creates PRs when upstream images change.

### CI/CD

- **Trigger**: CEL expressions detect which component directories changed and only build affected images.
- **PR builds**: Tagged `on-pr-{revision}`, expire after 5 days.
- **Push builds**: Tagged with the commit SHA and `latest`.
- **Pipeline**: `.tekton/pipelines/multi-arch-container-build.yaml` handles multi-architecture builds.
- **Renovate**: Monitors base image digests and Tekton bundle references, auto-creates update PRs.

## Adding a new image

See [docs/onboarding.md](docs/onboarding.md) for a step-by-step guide.
