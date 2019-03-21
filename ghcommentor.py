#!/usr/bin/env python
import sys
import logging
import argparse
import itertools
import requests
import json
from shell import shell
from github import Github
from logrusformatter import LogrusFormatter


"""
Login stuff
"""
global gh_token, jira_token, g
# Github
gh_token = "YOUR FANTASTIC GH TOKEN HERE"
# Jira
jira_username = "firstname.lastname@docker.com"
jira_token = "YOUR FANTASTIC JIRA TOKEN HERE"
# ---
g = Github(gh_token)

"""
getRemoteLink returns the GH issue associated with the given jira issue
specified as repository and issue number, for example:
- repository: 'FIELD'
- issue: '347'
"""
def getRemoteLink(jira_repository, jira_issue):
    r = requests.get('https://docker.atlassian.net/rest/api/2/issue/{0}-{1}/remotelink'.format(jira_repository, jira_issue),
                   auth=(
                        '{0}'.format(jira_username),
                        '{0}'.format(jira_token)
                       )
                )
    # Get the github url
    response_json = json.loads(r.text)
    gh_url = response_json[0]["object"]["url"]
    gh_issue_number = gh_url.split('/')[-1]
    return gh_issue_number


"""
generateComments generates comments for all issues within the given gh_repository.
The comment will feature the jira_issue that has linked the github issue.
"""
def generateComments(gh_repository, jira_repository, max_range):
    logging.info("Beginning comment generation for GH repo: {0} as associated by Jira repo: {1}".format(gh_repository, jira_repository))
    repo = g.get_repo(gh_repository)
    for jira_issue in range(1, max_range):
        # Get the Github issue associated with the jira_issue
        gh_issue_number = getRemoteLink(jira_repository, jira_issue)
        try:
            # If there's no github issue associated continue to the next
            # jira_issue
            len(gh_issue_number[0])
        except IndexError:
            continue
        logging.info("Generating comment in GH issue: {0} to associate it with {1}-{2}".format(gh_issue_number[0], jira_repository, jira_issue))
        issue = repo.get_issue(int(gh_issue_number[0]))
        try:
            issue.create_comment("This issue has moved to Jira.  The new issue can be found here: https://docker.atlassian.net/browse/{0}-{1}.".format(jira_repository, jira_issue))
        except github.GithubException.GithubException as e:
            logging.error("Unable to add comment to GH issue: {0}".format(e))
            continue

"""
Main
"""
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Comments on lotsa stuff \
    at the same time.')
    parser.add_argument("-g",
                        "--github-repo",
                        dest="github_repo",
                        required=True,
                        help="The docker/repository within GitHub, for \
                        example 'docker/escalation'")
    parser.add_argument("-j",
                        "--jira-repo",
                        dest="jira_repo",
                        required=True,
                        help="The Jira repository name to link the GitHub \
                        issues comments to, for example 'FIELD'")
    parser.add_argument("-c",
                        "--issue-count",
                        dest="issue_count",
                        help="Set the number of issues in the given Jira \
                        repository. If none is given a value of 1000 will \
                        be used.")
    parser.add_argument("--debug",
                        dest="debug",
                        action="store_true",
                        help="Enable debug logging")
    args = parser.parse_args()
    # Basic logging that matches logrus format
    fmt_string = "%(levelname)s %(message)-20s"
    fmtr = LogrusFormatter(colorize=True, fmt=fmt_string)
    logger = logging.getLogger(name=None)
    if not args.debug:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(fmtr)
    logger.addHandler(hdlr)
    # Validate given arguments
    gh_repo = args.github_repo.split("/")
    if not len(gh_repo[0]) > 0 and len(gh_repo[1]) > 0:
        logger.error("Given GitHub repo: {0} is not a valid org/repository".format(gh_repo))
        sys.exit(1)
    if args.issue_count:
        max_range = int(args.issue_count)
    else:
        max_range = 1000
    generateComments(args.github_repo, args.jira_repo, max_range)
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())
