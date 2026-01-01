#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: Jul 24th, 2022
# Version: 1.0
# https://peppe8o.com

import network, rp2
import time

def connect_wifi(ssid,password,country):
   rp2.country(country)
   wlan = network.WLAN(network.STA_IF)
   print("WLAN created, status:", wlan.status())
   wlan.config(pm = 0xa11140)  # Commented out to test
   wlan.active(True)
   print("Active, status:", wlan.status())
   time.sleep(1)  # Delay after active
   networks = wlan.scan()
   print("Scanned networks:", networks)
   wlan.connect(ssid, password)
   print("Connecting, status:", wlan.status())
   # Wait for connect or fail
   max_wait = 10
   while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
          break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)

   if wlan.status() != 3:
      raise RuntimeError('network connection failed')
   else:
      print('connected')
      status = wlan.ifconfig()
      print( 'ip = ' + status[0] )

      
   return status
