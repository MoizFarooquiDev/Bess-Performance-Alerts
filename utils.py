alarm_mapping = {
            0: "Offline",
            1: "Critical",
            2: "Major",
            3: "Minor / Warning",
            5: "Power-lost",
            7: "Com Error",
            8: "Info/Dont care",
            9: "ONM/Dont care"
            }

smtp_emails = {"gmail": "smtp.gmail.com",
               "outlook": "smtp.office365.com"}

email_type = "outlook" #"gmail"  #
email_user = "o" #"reonalert@gmail.com"
email_pwd = "" #"kxplzytvutukuvnf"

email_user = ''
email_pwd = ''
spark_user = ""
spark_pwd = ""
enfra_user = ""
enfra_pwd = ""

# indexes
index_preprocessed = "site-telco-processed-data"
index_preprocessed_cni = "site-cni-processed-data"
index_anomalies_telco = "site-report-anomalies"
index_insights_processed = "site-insights-processed"
index_anomalies_cni = "site-cni-report-anomalies"
index_events = "site-alarms"


# dynamo forms
insites_form = "e4dcd674-37e6-4276-90e6-11da1b6a5e5e"
emails_form = "016bb569-55cf-49da-95c2-113d05bac7dd"
event_transition_form = "6adc67e6-3a77-43d1-98a1-117f3aa4b72a"

# thresholds
active_min_elapsed_time = 3
rectifier_fan_elapsed_time = 0


class Message:
    greetings = "Dear Customer,\n\n"
    # ending = "\n\nRegards,\nSPARKTM - The Energy Platform"
    ending = "\n\nRegards,\nEngro Enfrashare NOC"

    def get(self, body):
        return self.greetings + body + self.ending


inactive_html = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Inactive Events generated on *DATE* for *TENANT* tenancy sites</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Engro Enfrashare NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

inactive_html_tawal = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Inactive Events occurred *Date* for Jazz tenancy sites</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>TAWAL NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from TAWAL.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – Intelligent Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

active_html = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Active Events having elapsed time more than *ELAPSED_TIME*h</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Engro Enfrashare NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

active_html_tawal = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Active Events occurred on *Date* for Jazz tenancy sites.</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>TAWAL NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from TAWAL.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – Intelligent Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''


particular_event_html = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Active *EVENT_NAME* Events having elapsed time more than *ELAPSED_TIME*h</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Engro Enfrashare NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''


particular_event_html = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Customer,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Active *EVENT_NAME* Events having elapsed time more than *ELAPSED_TIME*h</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Engro Enfrashare NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''


rectifier_stress_report_html = '''<html>
<head> </head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Customer,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached summary of Rectifier Stress Report for yesterday i-e, *DATE*</span>.</span><br>
<br>
*SUMMARY_TAGS*
<br>For more details, please follow the link below:<br> \
<a href=https://reon-spark-live.d3p0x8u6w6rznq.amplifyapp.com/rpt-analysis-1v0>Reon Spark Reporting Anomalies</a> \
<br><br><b>Regards,<br>SPARK<sup>TM</sup> - The Energy Platform</b>
</span></p>
</body>
</html>'''


battery_performance_report_html = '''<html>
<head> </head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Customer,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>We have analyzed *analyzed_sites* sites out of total *total_sites* sites and following is the summary</span>.</span><br>
<br>
*SUMMARY_TAGS*
<br>For more details, please follow the link below:<br> \
<a href=https://reon-spark-live.d3p0x8u6w6rznq.amplifyapp.com/rpt-analysis-1v0>Reon Spark Reporting Anomalies</a> \
<br><br><b>Regards,<br>SPARK<sup>TM</sup> - The Energy Platform</b>
</span></p>
</body>
</html>'''

insites_html = '''<html>
<head> </head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Customer,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>We have analyzed *analyzed_sites* sites from your portfolio and a total of *analyzed_insites* INSITES were generated! Here is a brief summary</span>:</span><br>
<br>
*SUMMARY_TAGS*
<br>For more details, please follow the link below:<br> \
<a href=https://develop.d3lg3aqm84jzdt.amplifyapp.com/telco-ms-insites-oper-1v0>Reon Insites Operator View</a> \
<br><br><b>Regards,<br>SPARK<sup>TM</sup> - The Energy Platform</b>
</span></p>
</body>
</html>'''

reports_html = '''<html>
<head> 
    <style>
        table, th, td {
            text-align: left;
            padding: 8px;
        }
    </style>
</head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Concerned,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find below today’s customer-wise SPARK Performance Report</span>:</span><br>
<br>
*REPORTS_TAGS*
<br><br><b>Regards,<br>SPARK<sup>TM</sup> - The Energy Platform</b>
</span></p>
</body>
</html>'''

Offline_Sites_report_html = '''<html>
<head> 
    <style>
        table, th, td {
            text-align: left;
            padding: 8px;
        }
    </style>
</head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Concerned,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find below the summary</span>:</span><br>
<br>
*REPORTS_TAGS*

<br><br><b>Regards,<br>Engro Enfrashare NOC<sup>TM</sup> </b>
</span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</span></p>
</body>
</html>'''


event_transition_html = '''<html>
<head> </head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Customer,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>We have analyzed *analyzed_sites* sites and following is the summary of event transition anomalies with respect to site category</span>.</span><br>
<br>
*SUMMARY_TAGS*
<br><br><b>Regards,<br>SPARK<sup>TM</sup> - The Energy Platform</b>
</span></p>
</body>
</html>'''

Inactive_html_zong = '''<html>
<head> </head>
<body>
<div style="mso-element:para-border-div;border:none;border-bottom:solid windowtext 1.0pt;mso-border-bottom-alt:solid windowtext .75pt;padding:0in 0in 1.0pt 0in">
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white">Dear Customer,</span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span>Please find attached Inactive Events occurred *Date* for Zong tenancy sites</span>.</span><br>
<br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Regards,</span></span><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><span style="background:white"><span>Enfrashare NOC<o:p>&nbsp;</o:p></span></span></span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Enfrashare.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – Intelligent Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

ES_events = '''<html>
<head> 
    <style>
        table, th, td {
            text-align: left;
            padding: 8px;
        }
    </style>
</head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Concerned,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span> *content* </span>:</span><br>
<br>

<br><br><b>Regards,<br>Engro Enfrashare NOC<sup>TM</sup> </b>
</span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

ES_events_MSLK = '''<html>
<head> 
    <style>
        table, th, td {
            text-align: left;
            padding: 8px;
        }
    </style>
</head>
<body>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E;background:white"><b>Dear Concerned,</b></span><span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
</span></p>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif;border:none;mso-border-bottom-alt:solid windowtext .75pt;padding:0in;mso-padding-alt:0in 0in 1.0pt 0in">
<span style="font-family:&quot;Segoe UI&quot;,sans-serif;color:#201F1E"><br>
<span style="background:white"><span> *content* </span>:</span><br>
<br>

<br><br><b>Regards,<br>Engro Enfrashare NOC<sup>TM</sup> </b>
</span></p>
</div>
<p class="MsoNormal" style="margin:0in 0in 8pt;font-size:10pt;font-family:Calibri, sans-serif">
<i><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:#AAAAAA;background:white">This email is a service from Engro Enfrashare(Pvt) Ltd.</span> Delivered by&nbsp;<a href="https://www.reonenergy.com/digital-solution/" target="_blank" data-auth="NotApplicable" data-linkindex="2"><span class="mark8o54adx3e"><span style="font-size:9.0pt;font-family:&quot;Verdana&quot;,sans-serif;color:black;border:none windowtext 1.0pt;mso-border-alt:none windowtext 0in;padding:0in;background:white;text-underline:none"><span data-markjs="true" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="">SPARK</span></span></span></a><sup>TM</sup>
 – The Energy Platform.<o:p>&nbsp;</o:p></i></p>
</div>
</body>
</html>'''

Customer_Reflex_sites = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Reflex Performance Report</title>
  </head>
  <body style="margin: 0; padding: 0; background-color: #f8f9fa">
    <table
      width="100%"
      cellpadding="0"
      cellspacing="0"
      border="0"
      bgcolor="#f8f9fa"
    >
      <tr>
        <td align="center" style="padding: 20px">
          <table
            width="700"
            cellpadding="0"
            cellspacing="0"
            border="0"
            bgcolor="#ffffff"
            style="border: 1px solid #dddddd; border-collapse: collapse"
          >
            <tr>
              <td align="center" style="padding: 30px 30px 10px 30px">
                <img
                  src="https://develop.d3lg3aqm84jzdt.amplifyapp.com/static/media/spark-with-tagline.c53fc348b907314afbf7.png"
                  alt="Spark Logo"
                  width="200"
                  style="display: block; margin-bottom: 20px"
                />
                <h2
                  style="
                    margin: 0;
                    color: #6f4ca5;
                    font-family: Arial, sans-serif;
                    font-size: 24px;
                  "
                >
                  REFLEX Performance Report
                  <br><span style="color: #000000; font-size: 16px;">*DATE*</span></br>
                </h2>
              </td>
            </tr>

            <!-- Section 1 -->
            <tr>
              <td style="padding: 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  1. Site & System Overview
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Site Name</td>
                    <td width="50%">*SiteName*</td>
                  </tr>
                  <tr>
                    <td width="50%">Commissioning Date</td>
                    <td width="50%">*Commissioning Date*</td>
                  </tr>
                  <tr>
                    <td width="50%">Contractual Power</td>
                    <td width="50%">*Contractual Power*</td>
                  </tr>
                  <tr>
                    <td width="50%">Installed Capacity</td>
                    <td width="50%">*Installed Capacity*</td>
                  </tr>
                  <tr>
                    <td width="50%">System Age</td>
                    <td width="50%">*System Age*</td>
                  </tr>
                  <tr>
                    <td width="50%">System Uptime (24h)</td>
                    <td width="50%">*System Uptime*</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 2 -->
            <tr>
              <td style="padding: 0px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  2. Daily Performance Summary
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Max. Active Power (Chg/Dschg)</td>
                    <td width="50%">*Max Active Power*</td>
                  </tr>
                  <tr>
                    <td width="50%">Max. Reactive Power (Chg/Dschg)</td>
                    <td width="50%">*Max Reactive Power*</td>
                  </tr>
               
                  <tr>
                    <td width="50%">Max. Apparent Power</td>
                    <td width="50%">*Max Apparent Power*</td>
                  </tr>
               
                  <tr>
                    <td width="50%">Charged Energy</td>
                    <td width="50%">*Energy Charged*</td>
                  </tr>
                  <tr>
                    <td width="50%">Discharged Energy</td>
                    <td width="50%">*Energy Discharged*</td>
                  </tr>
                  <tr>
                    <td width="50%">Operating Mode</td>
                    <td width="50%">*Operating Mode*</td>
                  </tr>
                  <tr>
                    <td width="50%">Daily Cycles</td>
                    <td width="50%">*Daily Cycles*</td>
                  </tr>
                  <tr>
                    <td width="50%">Cumulative Cycles</td>
                    <td width="50%">*Cumulative Cycles*</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 3 -->
            <tr>
              <td style="padding: 30px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  3. Environmental and Auxiliary Parameters
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Ambient Temperature (Avg)</td>
                    <td width="50%">*Ambient Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">Battery Temperature (Max/Min)</td>
                    <td width="50%">*Battery Room Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">PCS Temperature (Max)</td>
                    <td width="50%">*PCS Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">Auxiliary Consumption</td>
                    <td width="50%">*Auxiliary Consumption*</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 4 -->
            <tr>
              <td style="padding: 30px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  4. Asset Performance Management
                </p>

                <!-- Top part (2 columns) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th width="50%" align="left">Parameter</th>
                    <th width="50%" align="left">Value</th>
                  </tr>
                  <tr>
                    <td>Contract Status</td>
                    <td>*Contract Status*</td>
                  </tr>
                  <tr>
                    <td>Contract Date</td>
                    <td>*Contract Date*</td>
                  </tr>
                  <tr>
                    <td>Uptime Commitment</td>
                    <td>*Uptime Commitment*</td>
                  </tr>
                  <tr bgcolor="#e9ecef">
                    <td colspan="2" style="font-weight: bold; text-align: center;">
                      Corrective Maintenance
                    </td>
                  </tr>
                </table>

                <!-- Corrective Maintenance (4 columns, no top border) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    border-top: none;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#f8f9fa">
                    <th width="10%" align="left">TT ID#</th>
                    <th width="50%" align="left">Subject</th>
                    <th width="20%" align="left">Problem Start Date</th>
                    <th width="20%" align="left">Ageing</th>
                  </tr>
                  *CORRECTIVE_TICKETS*
                  <tr bgcolor="#e9ecef">
                    <td colspan="4" style="font-weight: bold; text-align: center;">
                      Preventive Maintenance
                    </td>
                  </tr>
                </table>

                <!-- Preventive Maintenance (4 columns, no top border) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    border-top: none;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#f8f9fa">
                    <th width="10%" align="left">WO ID#</th>
                    <th width="50%" align="left">Subject</th>
                    <th width="20%" align="left">Planned Start Date</th>
                    <th width="20%" align="left">Planned End Date</th>
                  </tr>
                  *WORK_ORDERS*
                </table>
              </td>
            </tr>


            <!-- Footer -->
            <tr>
              <td align="center" style="padding: 20px 30px 30px 30px">
                <p
                  style="
                    margin: 0;
                    font-family: Arial, sans-serif;
                    font-size: 9px;
                    color: #6c757d;
                  "
                >
                  This report has been auto generated by
                  <strong>SPARK</strong> | The Intelligent Energy Platform.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>

'''

Customer_BESS_sites = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Reflex Performance Report</title>
<style>
    * {
        box-sizing: border-box;
    }
    table {
        width: 100%;
        min-width: 600px;
        border-collapse: collapse;
        background-color: #fff;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: center;
        vertical-align: middle;
        white-space: nowrap;
    }
    th:first-child,
    td:first-child {
        width: 30%;
        text-align: left;
    }
    th {
        background-color: #d3c9e4;
        color: #000;
        white-space: nowrap;
        text-align: center;
        padding: 10px;
        font-size: 13px;
    }

    /* Fixed column widths to avoid header wrapping */
    th:nth-child(3), td:nth-child(3) {
        width: 140px;  /* Commissioning Date */
        white-space: nowrap;
    }

    th:nth-child(12), td:nth-child(12) {
        width: 180px;  /* Battery Rack SOC (Max/Min/Delta) */
        white-space: nowrap;
    }
    th:nth-child(13), td:nth-child(13) {
        width: 160px;  /* PCS Temperature (Max) */
        white-space: nowrap;
    }
    th:nth-child(14), td:nth-child(14) {
        width: 100px;  /* PCS Temperature (Max) */
        white-space: nowrap;
    }

    th:nth-child(17), td:nth-child(17) {
        width: 160px;  /* Battery Temperature (Max/Min) */
        white-space: nowrap;
    }

    th:nth-child(18), td:nth-child(18) {
        width: 100px;  /* Tickets */
        white-space: nowrap;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #f1f7ff;
    }

    @media screen and (max-width: 768px) {
        table {
            font-size: 12px;
        }
        th, td {
            padding: 6px;
        }
    }
</style>
</head>
<body style="margin: 0; padding: 100; background-color: #f8f9fa;">
<table align="center" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td align="center" style="padding: 10px 0;">
<img src="https://develop.d3lg3aqm84jzdt.amplifyapp.com/static/media/spark-with-tagline.c53fc348b907314afbf7.png" alt="Spark Logo" width="120" style="margin-bottom: 10px;" />
<h2 style="margin: 0; color: #6f4ca5; font-size: 18px;">REFLEX Performance Summary</h2>
<p style="margin: 0; color: #000; font-size: 14px;">*DATE*</p>
</td>
</tr>
<tr>
<td>
        *REPORTS_TAGS*
</td>
</tr>
</table>
</body>
</html>
'''

Soorty_Reflex_sites = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Reflex Performance Report</title>
  </head>
  <body style="margin: 0; padding: 0; background-color: #f8f9fa">
    <table
      width="100%"
      cellpadding="0"
      cellspacing="0"
      border="0"
      bgcolor="#f8f9fa"
    >
      <tr>
        <td align="center" style="padding: 20px">
          <table
            width="700"
            cellpadding="0"
            cellspacing="0"
            border="0"
            bgcolor="#ffffff"
            style="border: 1px solid #dddddd; border-collapse: collapse"
          >
            <tr>
              <td align="center" style="padding: 30px 30px 10px 30px">
                <img
                  src="https://develop.d3lg3aqm84jzdt.amplifyapp.com/static/media/spark-with-tagline.c53fc348b907314afbf7.png"
                  alt="Spark Logo"
                  width="200"
                  style="display: block; margin-bottom: 20px"
                />
                <h2
                  style="
                    margin: 0;
                    color: #6f4ca5;
                    font-family: Arial, sans-serif;
                    font-size: 24px;
                  "
                >
                  REFLEX Performance Report
                  <br><span style="color: #000000; font-size: 16px;">*DATE*</span></br>
                </h2>
              </td>
            </tr>

            <!-- Section 1 -->
            <tr>
              <td style="padding: 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  1. Site & System Overview
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Site Name</td>
                    <td width="50%">*SiteName*</td>
                  </tr>
                  <tr>
                    <td width="50%">Commissioning Date</td>
                    <td width="50%">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td width="50%" style="border-right: 1px solid #dee2e6; padding-right: 10px;"><b>Old:</b> *Commissioning Date*</td>
                          <td width="50%" style="padding-left: 10px;"><b>New:</b> *Commissioning Date2*</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td width="50%">Contractual Power</td>
                    <td width="50%">*Contractual Power*</td>
                  </tr>
                  <tr>
                    <td width="50%">Installed Capacity</td>
                    <td width="50%">*Installed Capacity*</td>
                  </tr>
                  <tr>
                    <td width="50%">System Age</td>
                    <td width="50%">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td width="50%" style="border-right: 1px solid #dee2e6; padding-right: 10px;"><b>Old:</b> *System Age*</td>
                          <td width="50%" style="padding-left: 10px;"><b>New:</b> *System Age 2*</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td width="50%">System Uptime (24h)</td>
                    <td width="50%">*System Uptime*</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 2 -->
            <tr>
              <td style="padding: 0px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  2. Daily Performance Summary
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Max. Active Power (Chg/Dschg)</td>
                    <td width="50%">*Max Active Power*</td>
                  </tr>
                  <tr>
                    <td width="50%">Max. Reactive Power (Chg/Dschg)</td>
                    <td width="50%">*Max Reactive Power*</td>
                  </tr>
               
                  <tr>
                    <td width="50%">Max. Apparent Power</td>
                    <td width="50%">*Max Apparent Power*</td>
                  </tr>
               
                  <tr>
                    <td width="50%">Charged Energy</td>
                    <td width="50%">*Energy Charged*</td>
                  </tr>
                  <tr>
                    <td width="50%">Discharged Energy</td>
                    <td width="50%">*Energy Discharged*</td>
                  </tr>
                  <tr>
                    <td width="50%">Operating Mode</td>
                    <td width="50%">*Operating Mode*</td>
                  </tr>
                  <tr>
                    <td width="50%">Daily Cycles</td>
                    <td width="50%">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td width="50%" style="border-right: 1px solid #dee2e6; padding-right: 10px;"><b>Old: </b>*Daily Cycles*</td>
                          <td width="50%" style="padding-left: 10px;"><b>New: </b>*Daily Cycles 2*</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td width="50%">Cumulative Cycles</td>
                    <td width="50%">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td width="50%" style="border-right: 1px solid #dee2e6; padding-right: 10px;"><b>Old:</b> *Cumulative Cycles*</td>
                          <td width="50%" style="padding-left: 10px;"><b>New:</b> *Cumulative Cycles 2*</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 3 -->
            <tr>
              <td style="padding: 30px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  3. Environmental and Auxiliary Parameters
                </p>
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th  align="left" width="50%">Parameter</th>
                    <th  align="left" width="50%">Value</th>
                  </tr>
                  <tr>
                    <td width="50%">Ambient Temperature (Avg)</td>
                    <td width="50%">*Ambient Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">Battery Temperature (Max/Min)</td>
                    <td width="50%">*Battery Room Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">PCS Temperature (Max)</td>
                    <td width="50%">*PCS Temperature*</td>
                  </tr>
                  <tr>
                    <td width="50%">Auxiliary Consumption</td>
                    <td width="50%">*Auxiliary Consumption*</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Section 4 -->
            <tr>
              <td style="padding: 30px 30px 0 30px">
                <p
                  style="
                    margin: 0 0 10px 0;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    font-weight: bold;
                    color: #343a40;
                  "
                >
                  4. Asset Performance Management
                </p>

                <!-- Top part (2 columns) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#e9ecef">
                    <th width="50%" align="left">Parameter</th>
                    <th width="50%" align="left">Value</th>
                  </tr>
                  <tr>
                    <td>Contract Status</td>
                    <td>*Contract Status*</td>
                  </tr>
                  <tr>
                    <td>Contract Date</td>
                    <td>*Contract Date*</td>
                  </tr>
                  <tr>
                    <td>Uptime Commitment</td>
                    <td>*Uptime Commitment*</td>
                  </tr>
                  <tr bgcolor="#e9ecef">
                    <td colspan="2" style="font-weight: bold; text-align: center;">
                      Corrective Maintenance
                    </td>
                  </tr>
                </table>

                <!-- Corrective Maintenance (4 columns, no top border) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    border-top: none;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#f8f9fa">
                    <th width="10%" align="left">TT ID#</th>
                    <th width="50%" align="left">Subject</th>
                    <th width="20%" align="left">Problem Start Date</th>
                    <th width="20%" align="left">Ageing</th>
                  </tr>
                  *CORRECTIVE_TICKETS*
                  <tr bgcolor="#e9ecef">
                    <td colspan="4" style="font-weight: bold; text-align: center;">
                      Preventive Maintenance
                    </td>
                  </tr>
                </table>

                <!-- Preventive Maintenance (4 columns, no top border) -->
                <table
                  width="100%"
                  cellpadding="8"
                  cellspacing="0"
                  border="1"
                  style="
                    border-collapse: collapse;
                    border-top: none;
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #212529;
                    border-color: #dee2e6;
                  "
                >
                  <tr bgcolor="#f8f9fa">
                    <th width="10%" align="left">WO ID#</th>
                    <th width="50%" align="left">Subject</th>
                    <th width="20%" align="left">Planned Start Date</th>
                    <th width="20%" align="left">Planned End Date</th>
                  </tr>
                  *WORK_ORDERS*
                </table>
              </td>
            </tr>


            <!-- Footer -->
            <tr>
              <td align="center" style="padding: 20px 30px 30px 30px">
                <p
                  style="
                    margin: 0;
                    font-family: Arial, sans-serif;
                    font-size: 9px;
                    color: #6c757d;
                  "
                >
                  This report has been auto generated by
                  <strong>SPARK</strong> | The Intelligent Energy Platform.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
'''
