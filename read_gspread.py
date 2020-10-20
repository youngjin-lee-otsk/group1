from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:/py/chatBot/group1/butterfly-257608-926179e2b552.json',
    scopes=scope
)

gc = gspread.authorize(credentials)

gc1 = gc.open("KYS_ButterflyProject").worksheet('Sample')
gc2 = gc1.get_all_values()
print(gc2)
print(gc2[0])
print('--------')
"""
[0] = ID
[1] = Command
[2] = Contents
[3] = Contents
""" 
"""
입력 : EMG_EDI
출력 : 'KT:123', 'YJ:456', 'SM:789'
"""
inputdata = input()
for idx, asd in enumerate(gc2):
    print('asd', asd)
    if asd[0] == inputdata:
        for idx2, zxc in enumerate(gc2[idx]):
            if idx2 > 1 :
                print (zxc)
                if zxc == "" :
                    break
        print("OK")
    #print(asd[0])
    #print(asd[1])
    #print(asd[2])
    #print(asd[3])
    #print(asd[4])
