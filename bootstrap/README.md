# bootstrap/

One-time setup actions that may require a token scope the autonomous agent doesn't have.

## If the fetch-sources workflow won't install via the autonomous PAT

The autonomous agent's GitHub PAT lacks `workflow` scope (this was the issue in the learning-thesis sibling repo). GitHub rejects the push with:

> refusing to allow a Personal Access Token to create or update workflow `.github/workflows/fetch-sources.yml` without `workflow` scope

This repo was scaffolded locally by Zack on a machine whose `gh` auth has `workflow` scope, so the initial push installs the workflow directly. **If the autonomous PAT later needs to modify `.github/workflows/fetch-sources.yml`, that push will fail.** Two options:

### Option A — install from your machine (preferred for one-off changes)

```bash
git pull
git add .github/workflows/fetch-sources.yml
git commit -m "Update fetch-sources workflow"
git push
```

### Option B — give the agent's PAT `workflow` scope

Regenerate the PAT used for autonomous runs with `workflow` scope added (classic token) or with `Workflows: read and write` (fine-grained token). Then the agent can install and update workflows on its own.

## Manual primary-source drops

You can also bypass the wishlist for any one-off source: drop the file in `sources-raw/` with the right `AUTHOR-YEAR-shortname.ext` filename, commit, push. The agent will read it on the next Saturday run.
