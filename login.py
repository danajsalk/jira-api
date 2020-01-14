from jira import JIRA

options = {
    'server': 'https://jira.arbfund.com'
}
jira = JIRA(options, basic_auth = (username, password))

