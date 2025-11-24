from APIs import *
from utils import *
from processing import *
from smtp import *
import datetime
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta
import traceback

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
    
def code_to_status(code):
    if code == 0:
        return "Out of Contract"
    elif code == 1:
        return "Under Contract"

def main():
    buffer = []
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    wo_date = today.strftime('%Y-%m-%d')
    report_date = today.strftime('%Y-%m-%d')
    display_date = today.strftime('%B %d, %Y')
    
    status, login_token = login_api("", "")
    Bess_sites = ["d9072f04-98f8-4434-a06e-8519f1984382",
                "386c7a57-6910-46e0-a550-7d7231dcdf342",
                "9d6525b1-f7b0-4cf9-8a4a-69bb89af9d1f",
                "f988f741-34dc-4bfa-aa15-24884636b142",
                "df6f7a5d-3c51-4527-9d38-3abc396648e2",
                "e712356f-2301-440d-82c7-1649991f743e",
                "e5c8300e-8ffa-41c3-a560-5fa8df42ad52"]
    
    Subjects = {
        "d9072f04-98f8-4434-a06e-8519f1984382": "Gatron HUB",
        "386c7a57-6910-46e0-a550-7d7231dcdf342": "SU8",
	    "9d6525b1-f7b0-4cf9-8a4a-69bb89af9d1f": "LCL Pezu",
        "f988f741-34dc-4bfa-aa15-24884636b142": "SU11",
        "df6f7a5d-3c51-4527-9d38-3abc396648e2": "SU13",
        "e712356f-2301-440d-82c7-1649991f743e": "AYCCL",
        "e5c8300e-8ffa-41c3-a560-5fa8df42ad52":"LCL Nooriabad"}
    
    Emails = {
        "d9072f04-98f8-4434-a06e-8519f1984382": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "386c7a57-6910-46e0-a550-7d7231dcdf342": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "9d6525b1-f7b0-4cf9-8a4a-69bb89af9d1f": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "f988f741-34dc-4bfa-aa15-24884636b142": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "df6f7a5d-3c51-4527-9d38-3abc396648e2": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "e712356f-2301-440d-82c7-1649991f743e": {"TO" : ["moiz.farooqui@reonenergy.com"]},
        "e5c8300e-8ffa-41c3-a560-5fa8df42ad52": {"TO" : ["moiz.farooqui@reonenergy.com"]}
    }

    
    data = get_Reflex_sites_KPI(report_date, report_date, Bess_sites)
    data_new = {}
    for i in data:
        data_new[i["_source"]["siteId"]] = i
    
    summary = get_Reflex_summary_KPI("2023-01-01", report_date, Bess_sites)
    summary_new = {}
    for i in summary["aggregations"]["sites"]["buckets"]:
        summary_new[i["key"]] = i

    tickets_df = moiz_tickets2()
    workorder_df = moiz_workorder(wo_date)
    # print(workorder_df)

    print("*********")
    for iter, siteid in enumerate(Bess_sites):
        try:
            subject = "REFLEX Performance Report — *SiteName* " #Email Subject
            subject = subject.replace("*SiteName*", Subjects[siteid])
            # if siteid != "df6f7a5d-3c51-4527-9d38-3abc396648e2": # Siteid for SU13
            site_json = site_db(login_token, siteid)[1]
            try:
                #Agening = (parser.parse(report_date) - parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date"])).days
                Agening1 = relativedelta(parser.parse(report_date), parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date"]))
                parts = []
                if Agening1.years:
                    parts.append(f"{Agening1.years}y")
                if Agening1.months:
                    parts.append(f"{Agening1.months}m")
                if Agening1.days:
                    parts.append(f"{Agening1.days}d")

                result_agening1 = ', '.join(parts) if parts else "0 days"
            except:
                Agening1 = 0

            try:
                #Agening = (parser.parse(report_date) - parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date"])).days
                Agening2 = relativedelta(parser.parse(report_date), parser.parse(site_json['siteInfo']['infoWidget']["BESS Commissioning Date 2"]))
                parts = []
                if Agening2.years:
                    parts.append(f"{Agening2.years} Y{'s' if Agening2.years > 1 else ''}")
                if Agening2.months:
                    parts.append(f"{Agening2.months} M{'s' if Agening2.months > 1 else ''}")
                if Agening2.days:
                    parts.append(f"{Agening2.days} D{'s' if Agening2.days > 1 else ''}")

                result_agening2 = ', '.join(parts) if parts else "0 days"
            except:
                Agening2 = 0
            

        # Filter tickets for this site
            site_tickets = tickets_df[tickets_df["site_id"].astype(str).str.contains(str(siteid), na=False)]

            if len(site_tickets) > 0:
                ticket_rows_html = ""
                for _, row in site_tickets.iterrows():
                    ticket_rows_html += f"""
                    <tr>
                        <td width="10%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['TT_ID']}</td>
                        <td width="50%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Subject']}</td>
                        <td width="20%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Problem_Start_Date']}</td>
                        <td width="20%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Ageing']}</td>
                        
                    </tr>
                    """
            else:
                ticket_rows_html = """
                <tr>
                    <td colspan="4" style="font-family: Arial, sans-serif; font-size: 12px; color: #6c757d; text-align: center;">
                        No open tickets
                    </td>
                </tr>
                """

            site_wo = workorder_df[workorder_df["site_id"].astype(str).str.contains(str(siteid), na=False)]

            if len(site_wo) > 0:
                wo_rows_html = ""
                for _, row in site_wo.iterrows():
                    wo_rows_html += f"""
                    <tr>
                        <td width="10%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['WO_ID']}</td>
                        <td  width="50%"style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Subject']}</td>
                        <td  width="20%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Planned_Start_Date']}</td>
                        <td  width="20%" style=" font-family: Arial, sans-serif; font-size: 13px; color: #212529;">{row['Planned_End_Date']}</td>
                        
                        
                    </tr>
                    """
            else:
                wo_rows_html = """
                <tr>
                    <td colspan="4" style="font-family: Arial, sans-serif; font-size: 12px; color: #6c757d; text-align: center;">
                    No open workorders
                    </td>
                </tr>
                """

            battery_capacity = site_json['siteInfo']['infoWidget'].get("BESS DC", "0")
            battery_capacity = convert_energy_to_kwh(battery_capacity)
            rated_power = site_json['siteInfo']['infoWidget'].get("BESS AC", "0")
            rated_power = convert_power_to_kw(rated_power)
            code = site_json['siteInfo'].get("BESSContract", "0")
            code = code_to_status(code)

            BessAc = site_json['siteInfo']['infoWidget'].get("BESS AC", "")
            BessDc = site_json['siteInfo']['infoWidget'].get("BESS DC", "")
            
            if siteid == "386c7a57-6910-46e0-a550-7d7231dcdf342":
                html = Soorty_Reflex_sites.replace("*DATE*", display_date)
            else:
                html = Customer_Reflex_sites.replace("*DATE*", display_date)
                
            html = html.replace("*SiteName*", str(data_new[siteid]["_source"]["siteName"].split("(")[0]) + "<br>(" + BessAc + "/" + BessDc + ")")
            html = html.replace("*Commissioning Date*", site_json['siteInfo']['infoWidget'].get("BESS Commissioning Date", "-"))
            html = html.replace("*Commissioning Date2*", site_json['siteInfo']['infoWidget'].get("BESS Commissioning Date 2", "-"))
            html = html.replace("*Contractual Power*", site_json['siteInfo']['infoWidget'].get("Contractual Power","-"))
            html = html.replace("*Installed Capacity*", BessDc)

            html = html.replace("*System Age*", result_agening1)
            if siteid == "386c7a57-6910-46e0-a550-7d7231dcdf342":
                html = html.replace("*System Age 2*", result_agening2)
            else:
                pass

            uptime = data_new[siteid]["_source"].get("BESS_Uptime", 0)
            html = html.replace("*System Uptime*", f"{uptime:,.2f} %")
            
            max_chg_pow = data_new[siteid]["_source"].get("BESS_Max_CHG_Power", 0)
            max_dschg_pow = data_new[siteid]["_source"].get("BESS_Max_DSCHG_Power", 0) if data_new[siteid]["_source"].get("BESS_Max_DSCHG_Power", 0) != 0 else data_new[siteid].get("Max_Discharge_Power", 0)
            chg_percent = (abs(max_chg_pow) / rated_power) * 100 if rated_power else 0
            dschg_percent = (max_dschg_pow / rated_power) * 100 if rated_power else 0
            html = html.replace("*Max Active Power*",f"{max_chg_pow:,.0f} kW ({chg_percent:,.2f} %) / "f"{max_dschg_pow:,.0f} kW ({dschg_percent:,.2f} %)")

            chg_rpower = data_new[siteid]["_source"].get("BESS_Max_CHG_RPower", 0)
            chg_rpower_percent = (abs(chg_rpower) / rated_power) * 100 if rated_power else 0
            dschg_rpower = data_new[siteid]["_source"].get("BESS_Max_DSCHG_RPower", 0)
            dschg_rpower_percent = (abs(dschg_rpower) / rated_power) * 100 if rated_power else 0
            if chg_rpower > 0:
                chg_rpower_display = "-"
            else:
                chg_rpower_display = f"{chg_rpower:,.0f} kVAr ({chg_rpower_percent:,.2f} %)"
            html = html.replace("*Max Reactive Power*",f"{chg_rpower_display} / {dschg_rpower:,.0f} kVAr ({dschg_rpower_percent:,.2f} %)")


            html = html.replace("*Max Apparent Power*",f"{data_new[siteid]['_source'].get('BESS_Max_SPower', 0):,.0f} kVA")
            html = html.replace("*Energy Charged*",f"{data_new[siteid]['_source'].get('BESS_Max_CHG_Energy', 0):,.0f} kWh")
            html = html.replace("*Energy Discharged*",f"{data_new[siteid]['_source'].get('BESS_Max_DSCHG_Energy', 0):,.0f} kWh")
            html = html.replace("*Operating Mode*","PQ: " + f"{data_new[siteid]['_source'].get('REFLEX_PQ_Contribution', 0):,.2f} %"+ " ; VSG: " + f"{data_new[siteid]['_source'].get('REFLEX_VSG_Contribution', 0):,.2f} %")
            html = html.replace("*Daily Cycles*",f"{data_new[siteid]['_source'].get('No_of_Cycle', 0):,.2f}")
            if siteid == "386c7a57-6910-46e0-a550-7d7231dcdf342":
                html = html.replace("*Daily Cycles 2*",f"{data_new[siteid]['_source'].get('No_of_Cycle_2', 0):,.2f}")
            else:
                pass

            html = html.replace("*Cumulative Cycles*",f"{data_new[siteid]['_source'].get('Total_Cycles', 0):,.2f}")
            if siteid == "386c7a57-6910-46e0-a550-7d7231dcdf342":
                html = html.replace("*Cumulative Cycles 2*",f"{data_new[siteid]['_source'].get('Total_Cycles_2', 0):,.2f}")
            else:
                pass
            
            try:
                html = html.replace("*Ambient Temperature*", str(round(data_new[siteid]["_source"].get("Amb_Temp", 0), 2)) + " °C")
            except:
                html = html.replace("*Ambient Temperature*", "0" + " °C")
            html = html.replace("*Auxiliary Consumption*",str(round(data_new[siteid]["_source"].get("Aux_Consumption", 0), 2)) + " kWh (" +str(round((abs(data_new[siteid]['_source'].get('Aux_Consumption', 0)) / battery_capacity) * 100, 2)) + "%)")            
            html = html.replace("*Battery Room Temperature*", str(round(data_new[siteid]["_source"].get("REFLEX_Batt_Max_Temp", 0), 2)) + " °C"\
+ " / " + str(round(data_new[siteid]["_source"].get("REFLEX_Batt_Min_Temp", 0), 2)) + " °C")
            html = html.replace("*PCS Temperature*", str(round(data_new[siteid]["_source"].get("REFLEX_PCS_Max_Temp", 0), 2)) + " °C")

            html = html.replace("*Contract Status*", str(code or ""))
            html = html.replace("*Contract Date*", site_json['siteInfo']['contract'].get("BESSContractDate", "-"))
            html = html.replace("*Uptime Commitment*", site_json['siteInfo'].get("UptimeComittement", "-"))

            html = html.replace("*CORRECTIVE_TICKETS*", ticket_rows_html)
            html = html.replace("*WORK_ORDERS*", wo_rows_html)

            
            TO = Emails[siteid]["TO"]
            CC = ["muhammad.hunain@reonenergy.com"]
            BCC = ["moiz.farooqui@reonenergy.com"]
        
            send_alert(TO, CC, BCC, subject, None, html)
        except:
            traceback.print_exc()
    
    print(f'Reports events alert at {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

if __name__ == "__main__":
    main()