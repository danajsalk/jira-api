
import copy 
import datetime
import getpass # for JIRA login
import pandas as pd
import pyodbc as c
import re
import time
import urllib

from ast import literal_eval
from cryptography.fernet import Fernet # for JIRA login
from jira import JIRA
from urllib import parse


jql = 'project in (test) AND created >= -1d ORDER BY created DESC'


MyKeys = {
# Standard Case Values Submitted
    'key'                        : 'Case_ID',
    'fields_issuetype_name'      : 'Type_Label',
    'fields_issuetype_description': 'Type_Description',
    'fields_issuetype_id'        : 'Issue_Type_ID',
    'fields_project'             : 'Which_Desk',
    'fields_priority_name'       : 'Priority',
    'fields_priority_id'         : 'Priority_ID',
    'fields_labels'              : 'Lables',
    'fields_status_name'         : 'Case_Status',
    'fields_status_description'  : 'Status_Description',
    'fields_summary'             : 'Case_Title',
    
# Who is Involved In Case
    'fields_reporter_displayName': 'Reported_By',
    'fields_reporter_active'     : 'Reporter_Active',
    'fields_assignee_displayName': 'Assignee',
    'fields_assignee_active'     : 'Assignee_Active',

# Case Dates
    'fields_created'             : 'Created',
    'fields_updated'             : 'Last_Updated', # case update date
    'fields_resolutiondate'      : 'Resolved_Date',
    'fields_resolution_description'      : 'Resolution_Description',
    'fields_duedate'             : 'Due_Date',
    'fields_lastViewed'          : 'Last_Viewed',
    'fields_timeZone'            : 'Time_Zone',
    
# Case Details
    'fields_description'         : 'Case_Description',
    'fields_issuelinks'          : 'Issue_Links', # LIST of Values
    'fields_timespent'           : 'Time_Spent',
    'fields_votes_votes'         : 'Case_Vote_Count',
    'fields_watches_watchCount'  : 'Watch_Count',
    'fields_comment_total'       : 'Comment_Count'
 }

key_list_header = list(MyKeys.values())

columns_dont_need = [
    'expand',
    'fields_iconUrl',

    '16x16', '24x24','32x32','48x48',
    'fields_author_avatarUrls_16x16',
    'fields_author_avatarUrls_24x24',
    'fields_author_avatarUrls_32x32',
    'fields_author_avatarUrls_48x48',
    'fields_assignee_avatarUrls_16x16',
    'fields_assignee_avatarUrls_24x24',
    'fields_assignee_avatarUrls_32x32',
    'fields_assignee_avatarUrls_48x48',
    'fields_creator_avatarUrls_16x16',
    'fields_creator_avatarUrls_32x32',
    'fields_creator_avatarUrls_24x24',
    'fields_creator_avatarUrls_48x48',
    'fields_colorName'
                    
                    ]

key_list_header = list(MyKeys.values())



def jira_login():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    username = input("Username: ").encode("utf-8")
    password = getpass.getpass().encode("utf-8")

    cipher_text_un = cipher_suite.encrypt(username)
    cipher_text_pw = cipher_suite.encrypt(password)

    ################ Configs -Decrypt imported file


    username = cipher_suite.decrypt(cipher_text_un).decode("utf-8", "strict")
    _这不是密码 = cipher_suite.decrypt(cipher_text_pw).decode("utf-8", "strict")

    def getCipherText():
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        username = input("Username: ").encode("utf-8")
        password = getpass.getpass().encode("utf-8")

        cipher_text_un = cipher_suite.encrypt(username)
        cipher_text_pw = cipher_suite.encrypt(password)

        encryption_list = [key.decode("utf-8"), cipher_text_un.decode("utf-8"), cipher_text_pw.decode("utf-8")]

        file = filepath  # Put full filepath here where you want encrypted password to be stored
        out_file = open(file, "w")

        for line in encryption_list:
            out_file.write(line)
            out_file.write("\n")
        out_file.close()
        
    options = {
        'server': 'https://jira.arbfund.com'
        }
    jira = JIRA(options, basic_auth = (username, password))


# Gets every issue using the JQL filter
def get_issues(jql, start_at=0, results_per_search=1000, get_all_issues=True):
    issue_list = jira.search_issues(jql, startAt=start_at, maxResults=results_per_search, expand='changelog')

    if get_all_issues:
        for start_at in range(results_per_search, issue_list.total, results_per_search):
            # start_at = start_at + results_per_search
            issue_list = issue_list + jira.search_issues(jql, startAt=start_at, maxResults=results_per_search,
                                                         expand='changelog')

    return issue_list


# Removes any NULL/Empty values to cut down intial data
def remove_empties_from_dict(a_dict):
    new_dict = {}
    for k, v in a_dict.items():
        if isinstance(v, dict):
            v = remove_empties_from_dict(v)
        if v is not None:
            new_dict[k] = v
    return new_dict


# have a list of dicionaries
# check for nested lists in values with nested dictionaries
# Pulls nested values adding it to it's own key so duplicates aren't deleted when dicts are elevated
def re_dict(d, new_dict, parent=None):
    for k, v in d.items():
        pname = str(k) if parent is None else parent + "_" + str(k)
        if isinstance(v, dict):
            re_dict(v, new_dict, pname)
        else:
            new_dict[pname] = v


# Pull nested dictionaries to one level
def elevate_nested_dicts(dictionary, parent=None):
    finished = False
    while not finished:
        finished = True
        dcopy = dictionary.copy()
        for key, val in dcopy.items():
            if isinstance(val, dict):
                finished = False
                elevate_nested_dicts(val.copy(), parent=dictionary)
                del dictionary[key]
            elif parent is not None:
                if key not in parent.keys():
                    parent[key] = val
                # del dictionary[key]
    return dictionary


# Replaces all headers with any in MyKeys
def column_data_edits(data_frame):
    empty_dict = {}
    for key, val in MyKeys.items():
        if str(key) in [str(i) for i in data_frame.columns]:
            empty_dict[str(key)] = val
    data_frame = data_frame.rename(index=str, columns=empty_dict)
    return data_frame

############################################################################

jira_login()

issues = get_issues(jql, results_per_search=1000)

# Create a list of cases from filter
issues_list = [] 
for i in issues:
    g = str(i)
    issues_list.append(g)

# New list pulling in all JIRA data for every issue
all_data=[]
for num, i in enumerate(issues_list):
    issue = jira.issue(i)
    all_data.append(issue.raw)

    filter_data = []
    for i in all_data:
        filter_dict = remove_empties_from_dict(i)
        filter_data.append(filter_dict)
   
    # Finds every instance of a nested dictionary, relabels key, val
    for m in filter_data:
        for k, v in m.items():
            if isinstance(v, list):
                for j in v:
                    if isinstance(j, dict):
                        new_dict = {}
                        re_dict(j, new_dict)
                        m[k] = new_dict

            elif isinstance(v, dict):
                new_dict = {}
                re_dict(v, new_dict, parent=k)
                m[k] = new_dict
            
        elevate_nested_dicts(m)
        
    df = pd.DataFrame.from_dict(filter_data)
    df = column_data_edits(df)
    
    for n in columns_dont_need:
        if n in df.columns:
            df.drop([n], axis=1, inplace=True)
    
print(len(df))
print("DONE")

