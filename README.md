# notificaiton-clockify-to-slack
This script get clockify time entries and send them to slack webhook notificaton.

## how to use

### prerequisite
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

### step0: Install python3.6.x
Omit

### step1: Install python packages

```
pip install -r requirements.txt
```

### step2: Configure a config.ini file

```
[clockify]
workspace_name = my workspace  # your Clockify workspace name
api_token = xxxxxxxxxx         # your Clockify api token

[slack]
webhook_url = https://hooks.slack.com/services/xxxxxx/xxxxxx/xxxxxxxxxxxxxx # slack webhook url
```

### step3: Run scrpit

```
$ python main.py
```
