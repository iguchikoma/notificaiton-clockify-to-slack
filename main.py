import requests
import json
import re
import sys
import urllib3
import datetime
import configparser
from urllib3.exceptions import InsecureRequestWarning
from dateutil.relativedelta import relativedelta

urllib3.disable_warnings(InsecureRequestWarning)

### Read config file
inifile = configparser.ConfigParser()
try:
    # open config file
    inifile.read('./config.ini', 'UTF-8')
 
    # read static parameter
    CLOCKIFY_WS = inifile.get('clockify', 'workspace_name')
    CLOCKIFY_API_TOKEN = inifile.get('clockify', 'api_token')
    CLOCKIFY_GET_INTERVAL = inifile.get('clockify', 'interval')
    SLACK_WEBHOOK_URL = inifile.get('slack', 'webhook_url')

except:
    print('Error occured while config.ini file reading')
    sys.exit(0)


# supported Clockify version 1.0
class ClockifyManager(object):

    def __init__(self, api_token, ws_name):
        self.url = 'https://api.clockify.me/api/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': api_token
        }
        # get ws_id
        workspaces = self.getWorkspaces()
        self.ws_id = None
        for workspace in workspaces:
            if workspace['name'] == ws_name:
                self.ws_id = workspace['id']
                break
        if self.ws_id == None:
            print('Error: workspace name might be wrong')
            sys.exit(0) 

    def getWorkspaces(self):
        res = requests.get(
            self.url + '/workspaces',
            headers=self.headers)
        if res.status_code == 500:
            print('Error: CLOCKIFY_API_TOKEN might be wrong')
            sys.exit(0) 
        # DEBUG
        # self.__printApiResult(res)
        return res.json()

    def getUsers(self):
        res = requests.get(
            self.url + '/workspace/' + self.ws_id + '/users',
            headers=self.headers)
        # DEBUG
        # self.__printApiResult(res)
        return res.json()

    def getTimeEntries(self, user_id, time):
        query_params = {
                'start': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        res = requests.get(
            self.url + '/workspaces/' + self.ws_id + '/user/' + user_id + '/time-entries',
            params=query_params,
            headers=self.headers)
        # DEBUG
        # self.__printApiResult(res)
        return res.json()

    def parseDescription(self, res):
        return res['description']

    def parseStartTime(self, res):
        date_str = res['timeInterval']['start']
        # convert from string-date to datetype-date
        return(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ"))

    def parseEndTime(self, res):
        date_str = res['timeInterval']['end']
        if date_str == None:
            return(None)
        # convert from string-date to datetype-date
        return(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ"))

    def utcToJst(self, data_utc):
        return(data_utc + datetime.timedelta(hours=9))

    def parseProjectId(self, res):
        return res['projectId']
    
    def getProjects(self):
        res = requests.get(
            self.url + '/workspaces/' + self.ws_id + '/projects',
            headers=self.headers)
        # DEBUG
        # self.__printApiResult(res)
        return res.json()

    def __printApiResult(self, res):
        print('URL:', res.url)
        print('Status Code:', res.status_code)
        print('Response Body:', json.dumps(res.json(), indent=4))


class SlackManager(object):

    def __init__(self):
        self.url = SLACK_WEBHOOK_URL

    def sendMsg(self, body):
        res = requests.post(
            self.url,
            data=json.dumps(body)
            )
        return

    def createMsgBody(self, user, pj_name, msg, start, end, color):
        body = {
            "username": user,
            "text": user + ": " + msg,
            "attachments": [
                {
                    "fields": [
                        {
                            "title": "Project",
                            "value": pj_name,
                            "short": True
                        },
        				{
                            "title": "Description",
                            "value": msg,
                            "short": True
                        },
        				{
                            "title": "StartTime",
                            "value": start,
                            "short": True
                        },
                        {
                            "title": "EndTime",
                            "value": end,
                            "short": True
                        }
                    ],
                    "color": color
                }
            ]
        }
        return(body)

if __name__ == '__main__':
    # create API client
    cm = ClockifyManager(CLOCKIFY_API_TOKEN, CLOCKIFY_WS)

    # create Slack API client
    sm = SlackManager()

    # set time (CLOCKIFY_GET_INTERVAL minutes ago)
    date = datetime.datetime.today() - relativedelta(minutes=int(CLOCKIFY_GET_INTERVAL))
   
    # get projects (use later for getting pj-name and pj-color)
    projects = cm.getProjects()

    # get users
    users = cm.getUsers()
    for user in users:
        # DEBUG
        print('-----------------------------')
        print(user['name'])
        timeEntries = cm.getTimeEntries(user['id'], date)
        for timeEntry in timeEntries:
            # DEBUG
            print(timeEntry)

            # get Clockify timeentry description
            msg = cm.parseDescription(timeEntry)

            # get time entry start time
            start = cm.parseStartTime(timeEntry)
            start_jst = cm.utcToJst(start)

            # get time entry end time
            end = cm.parseEndTime(timeEntry)
            if end == None:
                end_jst = None
            else:
                end_jst = cm.utcToJst(end)

            # set default pj_name
            pj_name = ''

            # set default color
            pj_color = '#F35A00'

            # get project id of the time entry
            pj_id = cm.parseProjectId(timeEntry)

            # search projects for getting pj name and color
            for project in projects:
                if pj_id == project['id']:
                    pj_name = project['name']
                    pj_color = project['color']
                    break

            # set end time
            if end_jst == None:
                end_time = None
            else:
                end_time = end_jst.strftime("%Y/%m/%d %H:%M:%S")

            # create body of slack message
            body = sm.createMsgBody(user['name'],
                                 pj_name,
                                 msg,
                                 start_jst.strftime("%Y/%m/%d %H:%M:%S"),
                                 end_time,
                                 pj_color)

            # send slack notification using webhook
            sm.sendMsg(body)
