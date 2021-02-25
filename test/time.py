import ntplib 
from time import ctime

ntpClient=ntplib.NTPClient()
response=ntpClient.request('pool.ntp.org')
print(ctime(response.tx_time))