# gh-mass-commentor
Simple tool to associate old GitHub issues with those in Jira.

## Usage
1. Build the patched `go-jira` tool to facilitate the interaction with Jira
to determine remote links:

```
go get github.com/squizzi/go-jira
cd $GOPATH/src/squizzi/go-jira
make install
cp ~/bin/jira ./jira
```

2. Edit the global `gh_token` variable with a `repo` scoped GitHub authtoken.

```python
"""
Login stuff
"""
global gh_token, jira_token, g
gh_token = "YOUR FANTASTIC TOKEN HERE"
g = Github(gh_token)
```

3. Install the requirements file:

```
pip3 install -r requirements.txt
```

4. Run it:

```
python3 ./ghcommentor.py -g docker/escalation -j FIELD -c 1200
```

Where `-g` is the Github repo, `-j` is the Jira repo and `-c` is the number of
Jira issues in the given Jira repo.

5. **Enjoy using this exceptionally hacky tool!!!**
