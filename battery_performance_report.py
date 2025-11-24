from APIs import login_api, get_site_info
from processing import *
from smtp import *
import datetime


def main():
    today = datetime.datetime.today()
    date = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    login_token = login_api(spark_user, spark_pwd)
    if login_token[0] == 200:
        login_token = login_token[1]
        sites_info = get_site_info(login_token)
        if sites_info[0] == 200:
            email_details = get_dynamo_form(login_token, emails_form)[1].get("process", {}).get(
                "battery_performance_report", {})
            sites_info = sites_info[1].get("sites_info", {})
            processed_df = get_es_data(date, date, index_preprocessed, None, [], preprocess=True)
            anomalies_df = get_es_data_anomalies(date, date, index_insights_processed, None, [], preprocess=True,
                                        query_filter={"terms": {"category.keyword": ["4",4]}},
                                        agg=None,
                                        # agg={"group_sub_cat": {"terms": {"field": "sub_cat.keyword"}}}
                                        )
            df, total_sites, analyzed_sites = get_battery_rpt_data(processed_df, sites_info)
            batt_anomalies = anomalies_df.groupby("detailCategory")["siteId"].count().to_dict()
            name_change = {'0' : 'Battery Warranty Warning HET', '1' : 'Battery Warranty Void HET', '2' : 'Battery Warranty Warning OC'}
            for key in batt_anomalies.keys():
                batt_anomalies[name_change.get(key)] = batt_anomalies.pop(key)
            
            summary_tags = "<span>Summary:</span><br>"
            for anomaly, count in batt_anomalies.items():
                summary_tags += f"<span>&emsp; •</span>" \
                                f"<span style='color:red;'> {count}</span>" \
                                f"<span> sites have Battery {anomaly} issue</span><br>"
            # html = battery_performance_report_html.replace("*DATE*", str(date))
            html = battery_performance_report_html.replace("*analyzed_sites*", str(analyzed_sites))
            html = html.replace("*total_sites*", str(total_sites))
            html = html.replace("*SUMMARY_TAGS*", summary_tags)
            subject = email_details.get("subject")
            TO = email_details.get("recipients", {}).get("to")
            CC = email_details.get("recipients", {}).get("cc")
            BCC = email_details.get("recipients", {}).get("bcc")
            send_alert(TO, CC, BCC, subject, None, html, df.to_csv(index=False), filename=f"battery-performance-report-{str(date)}.csv")
            print(f'Battery performance rpt alert at {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        else:
            print("no site info")
    else:
        print("no login")


if __name__ == '__main__':
    main()