import re
import requests
from bs4 import BeautifulSoup


def get_status(case_num):
    header = {"User-Agent":"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    resp = requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do',
                     headers=header,
                     data={"changeLocale":"",
                           "appReceiptNum":case_num,
                           "initCaseSearch":"CHECK STATUS"})
    try:
        resp_content = BeautifulSoup(resp.content, "lxml")
        resp_text = resp_content.find('div',"current-status-sec").text
        resp_text = resp_text.replace("Your Current Status:", "")
        resp_text = re.sub(r'[\t\n\r+]',"", resp_text)
        rs_info = resp_content.find('div', "rows text-center").text
        status = resp_text.strip()
        rs_info = rs_info.replace("\n", " ")
        all = re.findall(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}", rs_info)
        try:
            date = all[0]
        except:
            date = "N/A"

        form = rs_info[rs_info.find("Form ")+5: rs_info.find("Form ")+10]
        if  '-' not in form:
            form = 'MISC'
        return case_num, date, form, status
    except Exception as e:
        print(e)
        return case_num, "N/A", "N/A", "N/A"
