# gh-mass-commentor
Simple tool to associate old GitHub issues with those in Jira.

## Usage
1. Edit the global `gh_token`, `jira_username` and `jira_token` variables. The
`gh_token` should be `repo` scoped.

```python
"""
Login stuff
"""
global gh_token, jira_token, g
# Github
gh_token = "YOUR FANTASTIC GH TOKEN HERE"
# Jira
jira_token = "YOUR FANTASTIC JIRA TOKEN HERE"
jira_username = "firstname.lastname@docker.com"
```

3. Build an image using the new token values:

```
make
```

4. Run it:

```
docker run --rm -it squizzi/ghcommentor:latest -g docker/escalation -j FIELD -c 1200
```

Where `-g` is the Github repo, `-j` is the Jira repo and `-c` is the number of
Jira issues in the given Jira repo.
