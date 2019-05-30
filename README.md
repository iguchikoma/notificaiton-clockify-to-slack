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

[slack]
webhook_url = https://hooks.slack.com/services/xxxxxx/xxxxxx/xxxxxxxxxxxxxx # slack webhook url
```

### Step3: Run scrpit

```
$ python main.py
```
