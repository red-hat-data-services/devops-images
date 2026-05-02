---
name: onboarding
description: Walk through adding a new container image to the devops-images repo. Guides through creating the Containerfile, updating components.yaml, running generators, and setting up the ServiceAccount.
when_to_use: Adding a new image, new component, onboarding a new contributor
user-invocable: true
argument-hint: "[image-name]"
allowed-tools: Bash(uv *) Bash(which *) Bash(git *) Read
---

# Add a new image

You are guiding the user through adding a new container image to this repo. Follow the steps in [docs/onboarding.md](../../../docs/onboarding.md).

## Your approach

1. Ask the user what their new image should be called and what tools it needs to include.

2. Check that `uv` is available — they'll need it to run the generation scripts.

3. Confirm the target image repository already exists on `quay.io/rhoai-devops`.

4. Walk them through each step one at a time:
   - Create the directory and write a Containerfile
   - Add the entry to `config.yaml`
   - Run `uv run scripts/generate-pipelines.py` and `uv run scripts/generate-pds.py`
   - Explain what was generated and why

5. Ask if the image needs a build secret (e.g. SSH key for cloning a private repo). If so, explain the `additional_secret` field and that the secret must exist in the namespace.

6. Remind the user to apply the updated ProjectDevelopmentStream to the cluster: `oc apply -f .konflux/ProjectDevelopmentStream.yaml -n rhoai-tenant`

7. After all steps, summarize what they need to commit and what happens when they push.

Keep it conversational — one step at a time, confirm before moving on.
