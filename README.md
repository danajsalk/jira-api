# Interacting with the Jira API
<br>

## Summary
<br>
User interface to JIRA.

Clients interact with JIRA by constructing an instance of this object and calling its methods. For addressable resources in JIRA – those with “self” links – an appropriate subclass of Resource will be returned with customized update() and delete() methods, along with attribute access to fields. This means that calls of the form issue.fields.summary will be resolved into the proper lookups to return the JSON value at that mapping. Methods that do not return resources will return a dict constructed from the JSON response or a scalar value; see each method’s documentation for details on what that method returns.

https://jira.readthedocs.io/en/master/api.html


## Issue Store Formatting and Normalization
<br>
When accessing the Jira API, the field values are reported as JIRA objects. To grab all data from JIRA cases like you would when downloading cases straight from the API to excel you need to use `issue.raw`

```
# New list pulling in all JIRA data for every issue using issue.raw
all_data = [(jira.issue(i)).raw for num, i in enumerate(issues_list)]
```
This returns a dictionary of every value in a case. The JIRA_to_DF script removes empties from the dictionary and pulls out nested dictionary values to the top level. Key:Value pairs are used to switch out fields to something more recognizable. 

```
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
```
With the number of fields per case, it is easier to add fields to the ones you want to keep instead of trying to normalize every field value an issue creates. 

## Example Fields
<br>

The Jira library comes with many built in functions
   * issue.fields.project.key
   * issue.fields.issuetype.name
   * issue.fields.reporter.displayName
   * issue.fields.summary
   * issue.fields.project.id
   * issue.raw
   
   
## Run Directions
<br>

* Update the `jql` statement
    * jql = 'project in (test) AND created >= -1d ORDER BY created DESC'
* Enter your Username and Password
    * You only have to login once per session. If you want to rerun this script comment out `jira_login()`
