import requests


def login_api(username, password):
    body = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
        "x-api-key": ""
    }
    params = {
        "regId": "<device id for push notification>",
        "deviceName": "<device model>"
    }
    url = ""
    r = requests.post(url, params=params, headers=headers, json=body)
    status = r.status_code
    response = r.json()
    token = response["response"]["token"]
    return (status, token)


def telco_live_assets(token, site_id):
    params = {
        "siteId": site_id
    }
    headers = {
        "Authorization": token,
        "x-api-key": ""
    }

    url = ""
    r = requests.get(url, params=params, headers=headers)
    return (r.status_code, r.json())


def telco_analysis(token, site_id):
    params = {
        "siteId": site_id
    }
    headers = {
        "Authorization": token,
        "x-api-key": ""
    }

    url = ""
    r = requests.get(url, params=params, headers=headers)
    return (r.status_code, r.json())


def telco_data(login_token, tags_body, site, start, end, interval, aggregate):
    body = tags_body

    headers = {
        "Content-Type": "application/json",
        "Authorization": login_token,
        "x-api-key": ""
    }

    params = {
        "start": start,
        "end": end,
        "interval": interval,
        "site": site,
        "aggregation": aggregate
    }

    url = ""

    r = requests.post(url, params=params, headers=headers, json=body)
    status = r.status_code
    response = r.json()
    return status, response


def telco_active(login_token, params):
    headers = {
        "Content-Type": "application/json",
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""

    r = requests.get(url, params=params, headers=headers)
    status = r.status_code
    response = r.json()
    return status, response


def user_sites(login_token):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }

    url = ""

    r = requests.get(url, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)


def site_db(login_token, site):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    params = {
        "siteId": site
    }

    url = ""

    r = requests.get(url, headers=headers, params=params)
    status = r.status_code
    response = r.json()
    return (status, response)


def get_std_thresholds(login_token):

    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)


def get_site_info(login_token):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)


def reports_rerun(loginToken, sites, start, end):
    body={
        "sites":sites
    }
    headers={
        "Authorization": loginToken,
        "x-api-key":"",
        "Content-Type":"application/json"
    }
    params={
        "start":start,
        "end":end,
        "ingest":"true"
    }
    url=""
    r=requests.post(url,params=params,headers=headers,json=body)
    status=r.status_code
    return status


def get_dynamo_mapping(login_token, form_id):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = f""
    r = requests.get(url, headers=headers)
    status = r.status_code
    response = r.json()
    return status, response


def get_events(token, params):
    headers = {
        "Authorization": token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, params=params, headers=headers)
    return r.status_code, r.json()

def user_info(token, id):
    params = {
        "userId": id
    }
    headers = {
        "Authorization": token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, params=params, headers=headers)
    return r.status_code, r.json()

def get_hardware_health(login_token, params):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, params=params, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)
    
def get_ms_events(login_token, params):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, params=params, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)
    
def get_NOC_3(login_token, params):
    headers = {
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
    r = requests.get(url, params=params, headers=headers)
    status = r.status_code
    response = r.json()
    return (status, response)

def telco_active(login_token, params):
    headers = {
        "Content-Type": "application/json",
        "Authorization": login_token,
        "x-api-key": ""
    }
    url = ""
 
    r = requests.get(url, params=params, headers=headers)
    status = r.status_code
    response = r.json()
    return status, response
