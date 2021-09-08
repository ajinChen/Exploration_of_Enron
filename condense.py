import pyarrow as pa
import pandas as pd
import numpy as np
import os
import sys
import re

# function area
def get_content(pwd:str):
    counter = 0
    for root, dirs, files in sorted(os.walk(pwd)):
        for filename in files:
            if not filename.startswith('.'):
                filepath = os.path.join(root, filename)
                filepath = filepath.replace("\\", "/")
                fn = filepath.replace(pwd + '/', '')
                To_sub = []
                with open(filepath, "r", encoding='latin1') as f:
                    contents = f.read()
                info = {}
                info['date'] = contents.split('Date:', 1)[1].split('\n', 1)[0].strip()
                info['subject'] = contents.split('Subject:', 1)[1].split('\n', 1)[0].strip()
                try:
                    info['to'] = contents.split('Subject:', 1)[0].split('To:', 1)[1].strip()
                    info['from'] = contents.split('From:', 1)[1].split('\n', 1)[0].strip()
                except:
                    info['to'] = ''
                    info['from'] = ''
                addr_from = filter_email(info['from'])
                if filter(info) == True and addr_from != None:
                    for i in re.split('[,\n]', info['to']):
                        addr_to = filter_email(i)
                        if addr_to != None:
                            To_sub.append(addr_to)
                    if len(To_sub) != 0:
                        counter += 1
                        for to in To_sub:
                            To.append(to)
                            Date.append(info['date'])
                            Recipients.append(len(To_sub))
                            Subject.append(info['subject'])
                            filename_sub.append(fn)
                            Mail_id.append(counter)
                            From.append(addr_from)
    return

def filter(info:dict):
    if info['to'] == '' or info['from'] == '':
        return False
    return True


def filter_email(email:str):
    if '@enron.com' not in email:
        return None
    addr = email[0:email.index('@')]
    addr = addr.strip()
    if '<' in addr or '#' in addr or "/o" in addr:
        return None
    if "'" in addr:
        addr = addr.replace("'", "")
    if len(addr) > 0 and addr[0] == '.':
        addr = addr.strip('.')
    if len(addr) > 0 and addr[0] == '\\':
        addr = addr.replace('\\', '')
    if len(addr) == 0:
        return None
    return addr



# interactive code
root_pwd = sys.argv[1]
Mail_id = []
Date = []
From = []
To = []
Recipients = []
Subject = []
filename_sub = []

get_content(root_pwd)
records = {'MailID': Mail_id, 'Date': Date, 'From': From, 'To': To, 'Recipients': Recipients, 'Subject': Subject,
           'filename': filename_sub}
df_enron = pd.DataFrame(records)
df_enron['Date'] = pd.to_datetime(df_enron['Date'], errors='raise', utc=True)
df_enron['Date'] = df_enron['Date'].dt.date
df_enron.to_feather('enron.feather')
