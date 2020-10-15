from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:/Python/group1/butterfly-257608-926179e2b552.json',
    scopes=scope
)

gc = gspread.authorize(credentials)

gc1 = gc.open("KYS_ButterflyProject").worksheet('Sample')
gc2 = gc1.get_all_values()
print(gc2)
print(gc2[0])