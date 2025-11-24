from APIs import *
from utils import *
from processing import *
from smtp import *
import datetime
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta
import traceback
import requests
import re


def convert_power_to_kw(power_str):
    if "MW" in power_str:
        value = float(power_str.replace("MW", "").strip())
        return value * 1000
    elif "kW" in power_str:
        return float(power_str.replace("kW", "").strip())
    else:
        return 1
     
def convert_energy_to_kwh(energy_str):
    try:
        if "MWh" in energy_str:
            value = float(energy_str.replace("MWh", "").strip())
            return value * 1000
        elif "kWh" in energy_str:
            return float(energy_str.replace("kWh", "").strip())
        else:
            return float(energy_str.strip())  
    except:
        return 0
     
def style_delta_soc(chunk_soc_max_delta):
    try:
        soc_text = f"{chunk_soc_max_delta:.1f}"
        if chunk_soc_max_delta > 10:
            return f'<span style="color:red">{soc_text}</span>'
        return soc_text
    except:
        return "0"
     
def style_uptime(val):
    try:
        val = round(float(val), 2)
        if val < 100:
            return f'<span style="color:red">{val}</span>'
        return str(val)
    except:
        return str(val)


def main():
    buffer = []
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    report_date = today.strftime('%Y-%m-%d')
    status, login_token = login_api("", "")
    Bess_sites = ["d9072f04-98f8-4434-a06e-8519f1984382",
                "386c7a57-6910-46e0-a550-7d7231dcdf342",
                "9d6525b1-f7b0-4cf9-8a4a-69bb89af9d1f",
                "f988f741-34dc-4bfa-aa15-24884636b142",
                "df6f7a5d-3c51-4527-9d38-3abc396648e2",
                "e712356f-2301-440d-82c7-1649991f743e",
                "e5c8300e-8ffa-41c3-a560-5fa8df42ad52"]
    
    data = get_Reflex_sites_KPI(report_date, report_date, Bess_sites)
    data_new = {}
    for i in data:
        data_new[i["_source"]["siteId"]] = i

    def chunk_soc(data,col_mapping):
        result = {}
        for i in data:
            site_id = i["_source"]["siteId"]
            chunk_cols = [key for key in i["_source"].keys() if re.match(r'CHUNK\d+', key)]
            max_value = None
            max_col = None
            for col in chunk_cols:
                val = i["_source"][col]
                if max_value is None or val > max_value:
                    max_value = val
                    max_col = col
            mapped_col = col_mapping.get(max_col, max_col)
            result[site_id] = (mapped_col, ":", max_value)
        return result
        
    mapping = {
    "CHUNK1": "Chunk#01",
    "CHUNK2": "Chunk#02",
    "CHUNK3": "Chunk#03",
    "CHUNK4": "Chunk#04",
    "CHUNK5": "Chunk#05",
    "CHUNK6": "Chunk#06",
    "CHUNK7": "Chunk#07",
    "CHUNK8": "Chunk#08",
    "CHUNK9": "Chunk#09",
    "CHUNK10": "Chunk#10",
    "CHUNK11": "Chunk#11",
    "CHUNK12": "Chunk#12",
    }

    summary = get_Reflex_summary_KPI("2023-01-01", report_date, Bess_sites)
    summary_new = {}
    for i in summary["aggregations"]["sites"]["buckets"]:
        summary_new[i["key"]] = i


    
    tickets = moiz_tickets()


    tickets_new = {}
    for _, row in tickets.iterrows():
        for field in row["fields"]:
            if field["id"] == 26646193288857:
                site_id = field["value"]
                tickets_new.setdefault(site_id, []).append(row.to_dict())
                break

    print("*********")
    for iter, siteid in enumerate(Bess_sites):
        try:
            site_json = site_db(login_token, siteid)[1]
            try:
                #Agening = (parser.parse(report_date) - parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date"])).days
                Agening = relativedelta(parser.parse(report_date), parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date"]))
                parts = []
                if Agening.years:
                    parts.append(f"{Agening.years} year{'s' if Agening.years > 1 else ''}")
                if Agening.months:
                    parts.append(f"{Agening.months} month{'s' if Agening.months > 1 else ''}")
                if Agening.days:
                    parts.append(f"{Agening.days} day{'s' if Agening.days > 1 else ''}")


                result_agening = ', '.join(parts) if parts else "0 days"
            except:
                Agening = 0
                
            rated_power = site_json['siteInfo']['infoWidget'].get("BESS AC", "0")
            battery_capacity = site_json['siteInfo']['infoWidget'].get("BESS DC", "0")
            rated_power = convert_power_to_kw(rated_power)
            battery_capacity = convert_energy_to_kwh(battery_capacity)
            BessAc = site_json['siteInfo']['infoWidget'].get("BESS AC", "")
            BessDc = site_json['siteInfo']['infoWidget'].get("BESS DC", "")
            Max_dschg_pow = data_new[siteid]["_source"].get("BESS_Max_DSCHG_Power", 0) if data_new[siteid]["_source"].get("BESS_Max_DSCHG_Power", 0) != 0 else data_new[siteid].get("Max_Discharge_Power", 0)
            uptime = data_new[siteid]["_source"].get("BESS_Uptime", 0)
            tickets = tickets_new.get(siteid, [])
            ticket_ids = [str(ticket.get("id", "NA")) for ticket in tickets]
            ticket_ids_str = ", ".join(ticket_ids) if ticket_ids else "NA"
            max_soc_values = chunk_soc(data, mapping)
            max_soc = max_soc_values.get(siteid, (None, None, None))
            max_soc_value = max_soc[2]
            max_soc_col = max_soc[0]



            buffer.append({"S. No.": iter + 1,
                        "Site Name": str(data_new[siteid]["_source"]["siteName"].split("(")[0]) + "<br>(" + BessAc + "/" + BessDc + ")",
                        "Commissioning Date": site_json['siteInfo']['infoWidget'].get("BESS Commissioning Date", None), 
                        "Contractual Power": site_json['siteInfo']['infoWidget'].get("Contractual Power",None),
                        "System Uptime \n (%)": style_uptime(uptime),
                        "Max Charging Power \n (kW)": f'{data_new[siteid]["_source"].get("BESS_Max_CHG_Power", 0)} <br> ({round((abs(data_new[siteid]["_source"].get("BESS_Max_CHG_Power", 0)) / rated_power) * 100, 2)} %)',
                        "Max Discharging Power \n (kW)": f"{Max_dschg_pow} <br> ({round((Max_dschg_pow / rated_power) * 100, 2)} %)",
                        "Charging Energy \n (kWh)": data_new[siteid]["_source"].get("BESS_Max_CHG_Energy", 0),
                        "Discharging Energy \n (kWh)": data_new[siteid]["_source"].get("BESS_Max_DSCHG_Energy", 0),
                        "Daily Cycles": round(data_new[siteid]["_source"].get("No_of_Cycle", 0), 2),
                        "Total Cycles": round(data_new[siteid]["_source"].get("Total_Cycles", 0), 2),
                        "Battery Rack SOC \n (Max. Delta)": (f" {max_soc_col}: " if max_soc_col else "") + style_delta_soc(max_soc_value) + " %",
                        "Auxiliary Consumption \n (kWh)": f"{round(data_new[siteid]['_source'].get('Aux_Consumption', 0), 2)} <br> ({round((abs(data_new[siteid]['_source'].get('Aux_Consumption', 0)) / battery_capacity ) * 100, 2)} %)",
                        "Ageing": str(result_agening),
                        "Ambient Temperature \n (C)": f"{round(data_new[siteid]['_source'].get('Amb_Temp') or 0, 2)} C",
                        "PCS Temperature \n (Max)": str(round(data_new[siteid]["_source"].get("REFLEX_PCS_Max_Temp",0),2)) + " C",
                        "Battery Temperature \n (Max/Min)": str(round(data_new[siteid]["_source"].get("REFLEX_Batt_Max_Temp", 0), 2)) + " C" + " / " + str(round(data_new[siteid]["_source"].get("REFLEX_Batt_Min_Temp", 0), 2)) + " C",
                        "Tickets": ticket_ids_str
                        })



        except:
            traceback.print_exc()
        
    df = pd.DataFrame(buffer)
    df.columns = [col.replace("\n", "<br>") for col in df.columns]
    
    html = Customer_BESS_sites.replace("*DATE*", report_date)
    html_table = df.to_html(border=1, index=False, escape=False, justify="center")
    html = html.replace("*REPORTS_TAGS*", html_table)
    
    subject = "Reflex Performance Report"
    TO = ["moiz.farooqui@reonenergy.com"]
    CC = ["moiz.farooqui@reonenergy.com"]
    BCC = []
    send_alert(TO, CC, BCC, subject, None, html)
    print(f'Reports events alert at {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

if __name__ == "__main__":
    main()