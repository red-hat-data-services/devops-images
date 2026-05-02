# Adding a new image

## Prerequisites

- Access to the `red-hat-data-services` GitHub organization
- Push access to `quay.io/rhoai-devops`
- `uv` installed (for running generation scripts)

## Steps

### 1. Create the image directory

Create a new directory under `builds/` with a `Containerfile`:

```
mkdir builds/my-tool
```

Write your `Containerfile`. If your image extends base-runner (most do), use:

```dockerfile
ARG BASE_RUNNER=quay.io/rhoai-devops/base-runner:latest
FROM $BASE_RUNNER

# install your tools
RUN dnf install -y <packages>
```

The `BASE_RUNNER` arg is pinned in `builds/my-tool/argfile.conf` with a SHA256 digest for reproducible builds. Each image has its own `argfile.conf`.

### 2. Add to config.yaml

Add an entry under `components`:

```yaml
- name: devops-my-tool
  image_name: my-tool
  context: builds/my-tool
```

The fields:
- **name**: Konflux component name and Tekton PipelineRun prefix
- **image_name**: image name under `quay.io/rhoai-devops/`
- **context**: path to the directory containing the Containerfile (under `builds/`)

If your image needs a build secret (like tracer does for SSH access to a private repo), add:

```yaml
  additional_secret: <secret-name>
```

The secret must already exist in the `rhoai-tenant` namespace.

### 3. Regenerate configs

```bash
uv run scripts/generate-pipelines.py
uv run scripts/generate-pds.py
```

This produces:
- `.tekton/<name>-pull-request.yaml` — PipelineRun triggered on PRs
- `.tekton/<name>-push.yaml` — PipelineRun triggered on push to main
- `.konflux/ProjectDevelopmentStream.yaml` — updated with the new component

### 4. Commit and push

Commit the new directory, updated `config.yaml`, and all generated files. Open a PR — the pipeline will trigger automatically for PR validation builds.

Once merged to main, the push pipeline builds and tags the image with the commit SHA and `latest`.

## Updating an existing image

1. Edit the `Containerfile` in the component's directory.
2. If the base image changes, update the image's `argfile.conf` with the new digest (or let Renovate handle it).
3. Push to `main` — the pipeline triggers automatically for changed directories only.
