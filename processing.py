from APIs import get_events, telco_active

import datetime

import json
from pandas import json_normalize
import requests
import pandas as pd
import re
from utils import *


def add_missing_columns(df, required):
    missing = list(set(required) - set(df.columns))
    return pd.concat([df, pd.DataFrame(columns=missing)], axis=1)


def site_name2id(sname, login_token, sites):
    for site in sites:
        if site["name"] == sname:
            return site["siteId"]
    return None


def num_sort(test_string):
    try:
        num = list(map(int, re.findall(r'\d+', test_string)))
        return num[0] if len(num) > 0 else 0
    except: 
        return 0   
    

def get_dynamo_form(login_token, form_id):
    headers = {
        "Authorization": login_token,
        "x-api-key": "fWXOewHZVL4EX6q7qgv9H5v85SF96wLh7jAMsFCs"
    }
    url = f""
    r = requests.get(url, headers=headers)
    status = r.status_code
    response = r.json()
    return status, response


def get_insite_name(cat, subCat, detailCat, mapping):
    for _cat in mapping.get("category", {}):
        if _cat.get("code") == cat:
            for _subCat in _cat.get("subCategory", {}):
                if _subCat.get("code") == subCat:
                    for _detailCat in _subCat.get("detailCategory", {}):
                        if _detailCat.get("code") == detailCat:
                            return _detailCat.get("name", "NA")
    return "NA"

def get_inactive_processed(login_token, date, tenant, project, filter_sites=[], startdate=None):
    next_page = None
    all_df = []
    start = date
    if project == "Tawal":
        start = startdate#"2025-01-01"
    while(True):
        params = {
            "status": "inactive",
            "size": 10000,
            "start_date": start,
            "end_date": date,
            "ten": tenant,
            "clusterId": "176dfdfb-b1b2-58e6-ab59-abd5778c781b" # not being used anymore.. constant
        }
        if next_page is not None:
            params["page"] = next_page
        resp = get_events(login_token, params)
        if resp[0] == 200:
            temp = pd.DataFrame(resp[1].get("data"))
            if len(temp) == 0:
                break
            else:
                all_df.append(temp)
            next_page = resp[1].get("meta", {}).get("next_page")
            if next_page is None:
                break
        else:
            break
        
    df = pd.concat(all_df)
    if project == "Tawal":
        df = df[(df["event"] == "Load Disconnected") | (df["event"] == "Bus Voltage Low") | (df["event"] == "Mains Fail") | (df["event"] == "BLVD: LVD-2") | (df["event"] == "LLVD: LVD-1") | (df["event"] == "Site Down")]
        df = df[pd.to_datetime(df["end_time"]).dt.strftime('%Y-%m-%d') == date]
    
    if project != "Zong":
        df = df[df["cluster"] == project]
        
        
    index_to_remove = []
    if project == "Zong":
        for i, item in df.iterrows():
            if item["id"] not in filter_sites:
                index_to_remove.append(i)
        df = df.drop(index=index_to_remove)
        
    df["tenant_buffer"] = df.filter(regex="t[0-9]$").eq(tenant).apply(lambda x: x[x].first_valid_index(), 1) # consider only one tenant of same company on each site
    df["tenant_name"] = tenant
    df["tenant_id"] = df.apply(lambda x: x[f'{x.tenant_buffer}_id'], 1)
    # req_columns = ["tenant_name", "tenant_id", "region", "active", "site_name", "event", "event_des", "start_time", "end_time", "elapsed_time", "total_minutes", "update_at"]
    req_columns = ["region", "site_name", "tenant_id", "event", "event_des", "start_time", "end_time", "elapsed_time", "total_minutes"]
    
    df = add_missing_columns(df, req_columns)
    df = df[req_columns]
    df.columns = [c.title() for c in df.columns]
    df.to_csv("Inactive_tawal.csv")
    return df.reset_index(drop=True)


def get_active_processed(login_token, start, end, site_names, min_elapsed_time, event=None):
    dfs = {}
    params = {
        "status": "active",
        "size": 10000,
        "start_date": start,
        "end_date": end,
        #"status_event": "On-Air",
        #"timezone": "Asia/Karachi"
    }
    resp = telco_active(login_token, params)
    if resp[0] == 200:
        df = pd.DataFrame(resp[1])
        req_columns = ["region", "site_name", "event", "event_des", "start_time", "elapsed_time", "total_minutes"]
        df = add_missing_columns(df, req_columns)
        df = df[df.site_name.isin(site_names)]
        current = datetime.datetime.now().replace(microsecond=0)
        df.elapsed_time = pd.to_datetime(df['start_time']).apply(lambda x: current-x)
        df.total_minutes = df.elapsed_time.dt.total_seconds().div(60)
        df = df[df.total_minutes > min_elapsed_time*60]
        df = df[req_columns]
        if event is not None:
        #    df = df[df.event == event]
        
          if (isinstance(event, str)):
              df = df[df.event == event]
          else:
              df=df[df['event'].isin(event)]

        for region in df.region.unique():
            dfs[region] = df[df.region == region]
            dfs[region] = dfs[region].sort_values(by='total_minutes')
            dfs[region].columns = [c.title() for c in dfs[region].columns]
    return dfs

def get_active_processed_tawal(login_token, start, end, site_names, min_elapsed_time, event=None):
    dfs = {}
    params = {
        "status": "active",
        "size": 10000,
        "start_date": start,
        "end_date": end,
        "ten": "Jazz"
    }
    resp = telco_active(login_token, params)
    if resp[0] == 200:
        df = pd.DataFrame(resp[1])
        df.to_csv("active_tawal0.csv")
        req_columns = ["region", "site_name", "tenant_id", "event", "event_des", "start_time", "elapsed_time", "total_minutes"]
        df = add_missing_columns(df, req_columns)
        df = df[df.site_name.isin(site_names)]
        current = datetime.datetime.now().replace(microsecond=0)
        df.elapsed_time = pd.to_datetime(df['start_time']).apply(lambda x: current-x)
        df.total_minutes = df.elapsed_time.dt.total_seconds().div(60)
        df["tenant_buffer"] = df.filter(regex="t[0-9]$").eq("Jazz").apply(lambda x: x[x].first_valid_index(), 1) # consider only one tenant of same company on each site
        df["tenant_name"] = "Jazz"
        df.dropna(subset=["tenant_buffer"], inplace=True)
        df["tenant_id"] = df.apply(lambda x: x[f'{x.tenant_buffer}_id'], 1)
        df = df[req_columns]
        if event is not None:
        
          if (isinstance(event, str)):
              df = df[df.event == event]
          else:
              df=df[df['event'].isin(event)]
        df = df[(df["event"] == "Load Disconnected") | (df["event"] == "Bus Voltage Low") | (df["event"] == "Mains Fail") | (df["event"] == "BLVD: LVD-2") | (df["event"] == "LLVD: LVD-1") | (df["event"] == "Site Down")]
        df = df[pd.to_datetime(df["start_time"]).dt.strftime('%Y-%m-%d') == start]
        df.columns = [c.title() for c in df.columns]
        df.to_csv("active_tawal.csv")
    return df.reset_index(drop=True)

def get_es_data_anomalies(start: str, end: str, index: str, shardid: str, fields: list, site_ids: list = [], preprocess: bool = False,
                query_filter=None, agg=None, time_stamp="@timestamp", user: str = "", password: str = "") -> pd.DataFrame:
    stream = []
    query = {
        "_source": fields,
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "observationDate": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                "observationDate": {
                    "order": "asc"
                }
            }
        ]
    }

    if query_filter is not None:
        query["query"]['bool']["must"].append(query_filter)

    if agg is not None:
        query["aggs"] = agg

    if len(site_ids) != 0:
        query['query']['bool']['must'].append({"terms": {"siteId.keyword": site_ids}})

    if len(fields) == 0:
        del query["_source"]

    if shardid:
        indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/{index}-{shardid}-*/_search?scroll=15m"
    else:
        indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/{index}/_search?scroll=15m"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=("Hamza", "hamza$r3on"),
        json=query)

    if "_scroll_id" not in json.loads(es.content):
        return pd.DataFrame([])
    scroll_id = json.loads(es.content)['_scroll_id']
    data_stream = json.loads(es.content)['hits']['hits']

    for datum in data_stream:
        stream.append(datum)

    while True:
        es = requests.post(
            url="https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/_search/scroll",
            headers={"content-type": "application/json"},
            auth=(user, password),
            json={
                "scroll": "15m",
                "scroll_id": scroll_id
            })
        if "hits" in json.loads(es.content).keys():
            if "hits" in json.loads(es.content)['hits'].keys():
                data_stream = json.loads(es.content)['hits']['hits']
            else:
                break
        else:
            break
        if len(data_stream) == 0:
            break
        for datum in data_stream:
            stream.append(datum)
    data = json_normalize(stream)
    if preprocess:
        # data = data.iloc[:, 5:]
        data.columns = [re.sub("_source.|logger.", "", c) for c in data.columns]
        time = "@timestamp"
        # if time in data.columns:
        #     data[time] = pd.to_datetime(data[time])
    return data


def get_es_data(start: str, end: str, index: str, shardid: str, fields: list, site_ids: list = [], preprocess: bool = False,
                query_filter=None, agg=None, time_stamp="@timestamp", user: str = "", password: str = "") -> pd.DataFrame:
    stream = []
    query = {
        "_source": fields,
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            time_stamp: {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                time_stamp: {
                    "order": "asc"
                }
            }
        ]
    }

    if query_filter is not None:
        query["query"]['bool']["must"].append(query_filter)

    if agg is not None:
        query["aggs"] = agg

    if len(site_ids) != 0:
        query['query']['bool']['must'].append({"terms": {"siteId.keyword": site_ids}})

    if len(fields) == 0:
        del query["_source"]

    if shardid:
        indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/{index}-{shardid}-*/_search?scroll=15m"
    else:
        indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/{index}/_search?scroll=15m"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=("Hamza", "hamza$r3on"),
        json=query)

    if "_scroll_id" not in json.loads(es.content):
        return pd.DataFrame([])
    scroll_id = json.loads(es.content)['_scroll_id']
    data_stream = json.loads(es.content)['hits']['hits']

    for datum in data_stream:
        stream.append(datum)

    while True:
        es = requests.post(
            url="https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/_search/scroll",
            headers={"content-type": "application/json"},
            auth=(user, password),
            json={
                "scroll": "15m",
                "scroll_id": scroll_id
            })
        if "hits" in json.loads(es.content).keys():
            if "hits" in json.loads(es.content)['hits'].keys():
                data_stream = json.loads(es.content)['hits']['hits']
            else:
                break
        else:
            break
        if len(data_stream) == 0:
            break
        for datum in data_stream:
            stream.append(datum)
    data = json_normalize(stream)
    if preprocess:
        # data = data.iloc[:, 5:]
        data.columns = [re.sub("_source.|logger.", "", c) for c in data.columns]
        time = "@timestamp"
        # if time in data.columns:
        #     data[time] = pd.to_datetime(data[time])
    return data

def get_es_report_count(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {"terms" : {
                            "siteId.keyword": site_ids
                            }
                        }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
        # "aggs": {
        #     "COUNT": {
        #         "top_hits": {
        #             "size": 10,
        #             "_source": ["siteId"]
        #         }
        #     }
        # }
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-telco-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    return (json.loads(es.content)['hits']['total']['value'])

def get_es_Dtwin_count(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {"terms" : {
                            "siteId.keyword": site_ids
                            }
                    },
                    {
                        "terms" : {
                            "dTwin" : [1]
                            }
                    }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
        # "aggs": {
        #     "COUNT": {
        #         "top_hits": {
        #             "size": 10,
        #             "_source": ["siteId"]
        #         }
        #     }
        # }
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-telco-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    return (json.loads(es.content)['hits']['total']['value'])

def get_es_forecast_count(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                      "terms" : {
                            "siteId.keyword": site_ids
                            }
                    },
                    {
                      "exists" : {
                            "field" : "logger.load_forecast"
                            }
                    }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ],
        "aggs": {
            "Unique_Count": {
                "cardinality": {
                        "field" : "siteId.keyword"
                        }
            }
        }
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-telco-cluster-*/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    return (json.loads(es.content))["aggregations"]["Unique_Count"]["value"]

def get_es_solar_count(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                      "terms" : {
                            "siteId.keyword": site_ids
                            }
                    },
                    {
                      "exists" : {
                            "field" : "analysis.SOLAR_YIELD.is_outlier"
                            }
                    }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-telco-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    # print("Solar:", (json.loads(es.content))['hits']['total']['value'])
    return (json.loads(es.content))['hits']['total']['value']

def get_es_battery_count(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                      "terms" : {
                            "siteId.keyword": site_ids
                            }
                    },
                    {
                      "exists" : {
                            "field": "battFlag"
                            }
                    }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-telco-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    # print("Batt:", (json.loads(es.content))['hits']['total']['value'])
    return (json.loads(es.content))['hits']['total']['value']

def get_rectifier_rpt_data(_df, sites_info):
    df = _df.copy()
    df = df.filter(regex='^RECT|siteName|siteId')
    df = df[sorted(df.columns)]
    site_names = df.pop("siteName")
    df.insert(0, "siteName", site_names)
    df.insert(loc=1,
                    column='RECT_BRAND',
                    value=df["siteId"].apply(
                        lambda x: sites_info.get(x, {}).get("infoWidget", {}).get("Rectifier Brand")))
    df.insert(loc=2,
                    column='RECT_QTY',
                    value=df["siteId"].apply(
                        lambda x: sites_info.get(x, {}).get("infoWidget", {}).get("Rectifier Qty")))
    df.insert(loc=3,
                    column='RECT_CAP',
                    value=df["siteId"].apply(
                        lambda x: sites_info.get(x, {}).get("infoWidget", {}).get("Rectifier Capacity")))
    df.drop(columns=['siteId'], inplace=True)
    return df


def get_battery_rpt_data(_df, sites_info):
    df = _df.copy()
    df = df.filter(regex=r'^BATT_SOC(?:\d+)_min$|'
                         r'^BATT_ENVTEMP(?:\d+)_max$|'
                         r'^BATT_CELLTEMP(?:\d+)_max$|'
                         r'^BATT_CURR_(?:\d+)_max$|'
                         'siteName|'
                         'siteId|'
                         'NbBattDischargeCycles')
    cols = sorted(df.columns, key=num_sort)
    mapping = {
        r'BATT_CELLTEMP(\d+)_max$': "B?CT",
        r'BATT_ENVTEMP(\d+)_max$': "B?ET",
        r'BATT_CURR_(\d+)_max$' : "B?CURR",
        r'BATT_SOC(\d+)_min$': "B?SOC"
    }
    new_cols = {}
    cols_seq = []
    for pattern, value in mapping.items():
        iteration = 1
        for c in cols: # could be used map function
            # if iteration <= 15:         
            result = re.match(pattern, c)
            if result is not None:
                num = result.groups()[0]
                new_cols[c] = value.replace("?", str(iteration))
                iteration = iteration + 1
                cols_seq.append(new_cols[c])
                
    new_cols['NbBattDischargeCycles'] = 'Cycles'
    df = df.rename(columns=new_cols)
    cols_seq.insert(0, "siteName")
    cols_seq.insert(1, "siteId")
    cols_seq.append("Cycles")
    df = df[cols_seq]
    df.insert(loc=1,
                    column='BATT_BRAND',
                    value=df["siteId"].apply(
                        lambda x: sites_info.get(x, {}).get("infoWidget", {}).get("Battery Brand")))
    df.insert(loc=2,
                    column='BATT_CAP',
                    value=df["siteId"].apply(
                        lambda x: sites_info.get(x, {}).get("infoWidget", {}).get("Battery Capacity")))
    df.drop(columns=['siteId'], inplace=True)
    analyzed_sites = df[new_cols.values()].notna().any(1).sum()
    total_sites = df.shape[0]
    return df, total_sites, analyzed_sites

def get_Reflex_sites_KPI(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                        "terms": {
                            "siteId.keyword": site_ids
                        }
                    }
                    # {
                    #   "exists" : {
                    #         "field": "BESS_Uptime"
                    #         }
                    # }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-cni-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    # print(es.content)
    return (json.loads(es.content))["hits"]["hits"]

def get_Reflex_summary_KPI(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                        "terms": {
                            "siteId.keyword": site_ids
                        }
                    }
                    # {
                    #   "exists" : {
                    #         "field": "BESS_Uptime"
                    #         }
                    # }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ],
        "aggs": {
            "sites": {
                        "terms": {
                            "field": "siteId.keyword",
                            "size": 10000
                            },
                        "aggs": {
                            "totalcycles": {
                                "sum": {
                                    "field": "No_of_Cycle"
                                         }
                                     }
                                }
                    }
                }
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-cni-processed-data/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    # print(json.loads(es.content))
    return (json.loads(es.content))

def get_alarm_ES(start: str, end: str, site_ids: list = [], user: str = "", password: str = ""):
    query = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start,
                                "lte": end,
                                "time_zone": "Asia/Karachi"
                            }
                        }
                    },
                    {
                      "terms" : {
                            "id.keyword": site_ids
                            }
                    },
                    {
                      "term" : {
                            "event_des.keyword": "Site is Offline"
                            }
                    }
                ]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
    }
    indexUrl = f"https://1ceb0ba8c26d49a4813e95550996d280.ap-southeast-1.aws.found.io:9243/site-alarms/_search"

    es = requests.post(
        url=indexUrl,
        headers={"content-type": "application/json"},
        auth=(user, password),
        json=query)
    data = (json.loads(es.content))['hits']['hits']
    df = pd.json_normalize(data)
    df.columns = [re.sub("_source.|logger.", "", c) for c in df.columns]
    df = df.iloc[:, 4:]
    return df


def preprocess_events(df, site_sources, sites_list):
    df.elapsed_time = pd.to_timedelta(df.elapsed_time)
    df.start_time = pd.to_datetime(df.start_time).dt.tz_localize(None)
    df['end_time'] = df.start_time + df.elapsed_time
    df = df.sort_values(by=["site_name", "start_time"]).reset_index(drop=True)
    df['source'] = df.groupby('site_name')['site_name'].transform(lambda x:
                                                                  [set(site_sources.get(site_name2id(x.iloc[0], None, sites_list), {}).get(
                                                                      "site_source", []))] * len(x))
    return df


def get_next_possible_events(transition_details, source_name_mapping, source, event):
    source_cat = source_name_mapping.get(frozenset(source))
    next_possible_event = transition_details.get(source_cat, {}).get("transition_states", {}).get(event, {}).get("next", [])
    return next_possible_event, source_cat


def get_event_transition_anomalies(df, login_token):
    event_details = get_dynamo_form(login_token, event_transition_form)[1]
    transition_details = event_details.get("cat_wise_details", {})
    focused_events = event_details.get("focused_events", [])
    source_name_mapping = {frozenset(v.get('sources')): k for k, v in transition_details.items()}
    df.loc[df.groupby('site_name').start_time.idxmax(), "last_packet_site"] = True
    df_events = df[df.event.isin(focused_events)].copy()
    df_other = df[~ df.event.isin(focused_events)].copy()
    df_events[["next_possible_events", "site_category"]] = df_events[["event", "source"]].apply(lambda x:
                                                                                                get_next_possible_events(
                                                                                                    transition_details,
                                                                                                    source_name_mapping,
                                                                                                    x["source"],
                                                                                                    x["event"]),
                                                                                                axis=1,
                                                                                                result_type='expand')
    df_events["next_focused_event"] = df_events.event.shift(-1)
    df_events["invalid_pattern"] = df_events.apply(lambda x: int((x.next_focused_event not in x.next_possible_events) &
                                                                 (pd.notna(x.next_focused_event)) &
                                                                 (x.last_packet_site is not True) &
                                                                 (len(x.next_possible_events) > 0)), 1)
    df_final = pd.concat([df_events, df_other])
    df_final["Event_Transition"] = df_final.apply(
        lambda x: f'{x.event} -> {x.next_focused_event}' if x.invalid_pattern == 1 else '', 1)
    df_final = df_final.sort_values(by=["site_name", "start_time"]).reset_index(drop=True)
    df.to_csv("test_events.csv", index=False)
    df_final = df_final[["site_name", "start_time", "end_time", "elapsed_time", "site_category", "source" , "event", "next_focused_event", "next_possible_events", "invalid_pattern", "Event_Transition"]]
    return df_final

class Zendesk:
    def __init__(self):
        self._url = "https://reonenergylimited.zendesk.com/api/v2/"
        self._user = ""
        self._password = ''
        self._headers = {'content-type': 'application/json'}

    def getTickets(self, query, page=1, url=None):
        url = url or self._url
        full_url = f'{url}search?query={query}&page={page}'
        return requests.get(url=full_url, auth=(self._user, self._password), headers=self._headers)

class Zendesk:
    def __init__(self):
        self._url = "https://reonenergylimited.zendesk.com/api/v2/"
        self._user = ""
        self._password = ''
        self._headers = {'content-type': 'application/json'}

    def getTickets(self, query, page=1, url=None):
        url = url or self._url
        full_url = f'{url}search?query={query}&page={page}'
        return requests.get(url=full_url, auth=(self._user, self._password), headers=self._headers)

    def getworkorders(self, query,start, page=1, url=None):
        url = url or self._url
        full_url = f'{url}search?query={query} created_at>={start} created_at<={start} &page={page}'
        return requests.get(url=full_url, auth=(self._user, self._password), headers=self._headers)
    
def moiz_tickets():
    zendesk = Zendesk()
    field_values = [
        "PCS",
        "BESS Local Controller",
        "Battery Racks",
        "BESS UPS",
        "HVAC/Chiller",
        "Transformer",
        "LV/MV Panel"
    ]

    results = []
    seen_ids = set()

    for value in field_values:
        page = 1
        nextpage = None
        while nextpage is not None or page == 1:
            query = (
                f'tags:ttm,rel,cni '
                f'custom_field_30404546513305:"{value}" '
                f'custom_field_26602125194777:"open"'
            )
            response = zendesk.getTickets(query=query, page=page, url=nextpage)
            data = json.loads(response.content)

            if "results" not in data:
                break

            for ticket in data["results"]:
                if ticket["id"] not in seen_ids:
                    seen_ids.add(ticket["id"])
                    results.append(ticket)

            nextpage = data.get("next_page")
            page += 1

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    return df

def format_datetime(dt_str):
    """Convert ISO datetime string to 'datetime object'"""
    if not dt_str:
        return None
    try:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")  # with microseconds
    except ValueError:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")  # without microseconds
    
def format_timedelta(td):
    """Format timedelta into days, hrs, mins"""
    days = td.days
    hrs, rem = divmod(td.seconds, 3600)
    mins = rem // 60
    return f"{days}d {hrs}h {mins}m"

def moiz_tickets2():
    zendesk = Zendesk()
    field_values = [
        "PCS",
        "BESS Local Controller",
        "Battery Racks",
        "BESS UPS",
        "HVAC/Chiller",
        "Transformer",
        "LV/MV Panel"
    ]

    results = []
    seen_ids = set()
    today = datetime.datetime.utcnow()

    for value in field_values:
        page = 1
        nextpage = None
        while nextpage is not None or page == 1:
            query = (
                f'tags:ttm,rel,cni '
                f'custom_field_30404546513305:"{value}" '
                f'custom_field_26602125194777:"open"'
            )
            response = zendesk.getTickets(query=query, page=page, url=nextpage)
            data = json.loads(response.content)

            if "results" not in data:
                break

            for ticket in data["results"]:
                if ticket["id"] not in seen_ids:
                    seen_ids.add(ticket["id"])
                    problem_start = None
                    status = None
                    site = None

                    for f in ticket.get("fields", []):
                        if f["id"] == 26599691285017:
                            problem_start = format_datetime(f["value"])
                        
                        elif f["id"] == 19258710906905:
                            status = f["value"]
                        elif f["id"] == 26646193288857:
                            site = f["value"]
                        elif f["id"] == 26599375708185:
                            subject = f["value"]

                    # calculate ageing if problem_start available
                    ageing = None
                    if problem_start:
                        td = today - problem_start
                        ageing = format_timedelta(td)

                    results.append({
                        "TT_ID": ticket["id"],
                        "Status": ticket["status"],
                        "Subject": subject,
                        "Problem_Start_Date": problem_start.strftime("%d-%m-%Y") if problem_start else None,
                        "site_id": site,
                        "Ageing": ageing
                    })

            nextpage = data.get("next_page")
            page += 1

    df = pd.DataFrame(results)
    return df

def moiz_workorder(start):
    zendesk = Zendesk()
    field_values = ["Reflex"]

    results = []
    seen_ids = set()
    
    for value in field_values:
        page = 1
        nextpage = None
        while nextpage is not None or page == 1:
            query = (
                f'tags:rel,cni '
                f'custom_field_13064842056217:"Reflex"'
            
            )
            response = zendesk.getworkorders(query=query,start= start, page=page, url=nextpage)
            data = json.loads(response.content)

            if "results" not in data:
                break

            for ticket in data["results"]:
                if ticket["id"] in seen_ids:
                    continue

                seen_ids.add(ticket["id"])

                planned_start = None
                planned_end = None
                status = None

                for f in ticket.get("fields", []):
                    if f["id"] == 19263707155481:
                        planned_start = format_datetime(f["value"])
                    elif f["id"] == 19263721624345:
                        planned_end = format_datetime(f["value"])
                    elif f["id"] == 19258710906905:
                        status = f["value"]
                    elif f["id"] == 26646193288857:
                        site = f["value"]

                results.append({
                    "WO_ID": ticket["id"],
                    "Status": status,
                    "Subject": ticket["subject"],
                    "Planned_Start_Date": planned_start.strftime("%d-%m-%Y") if planned_start else None,
                    "Planned_End_Date": planned_end.strftime("%d-%m-%Y") if planned_end else None,
                    "site_id": site
                })

            nextpage = data.get("next_page")
            page += 1

    df = pd.DataFrame(results)
    return df