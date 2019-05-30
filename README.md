# notificaiton-clockify-to-slack
This script get clockify time entries and send them to slack webhook notificaton.

## Sample result
<img width="491" alt="sample-result" src="https://user-images.githubusercontent.com/2556855/58643035-758c1500-8339-11e9-942f-51196b336764.png">

## How to use

### Prerequisite
This script is python program.

```
# python
version 3.6.x

# python packages
configparser
python-dateutil
requests
urllib3
```

### Step0: Install python3.6.x
Omit

### Step1: Install python packages

```
pip install -r requirements.txt
```

### Step2: Configure a config.ini file

```
[clockify]
workspace_name = my workspace  # your Clockify workspace name
api_token = xxxxxxxxxx         # your Clockify api token
interval = 5                   # time(min.) should the same value of cron preodic time for this script
[slack]
webhook_url = https://hooks.slack.com/services/xxxxxx/xxxxxx/xxxxxxxxxxxxxx # slack webhook url
```

### Step3: Run scrpit

```
$ python main.py
```

### Step4: Set the script in the cronjob
You should configure that the periodic time of the cronjob is the same as the interval in the config.ini file.
```
*/5 * * * * /home/ubuntu/.pyenv/shims/python /home/ubuntu/notification-clockify-to-slack/main.py >> /home/ubuntu/success.log 2>> /home/ubuntu/fail.log
```
