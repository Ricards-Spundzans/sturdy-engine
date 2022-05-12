
#       Importejamie paplašinājumi


from cgitb import text
from distutils.command.build import build
from http.client import FOUND
from logging import root
from multiprocessing.connection import wait
from operator import ge, le
import os, re
import pickle
import fitz
from PIL import Image
import io
import aspose.words as aw

import re   # regular expression
from sys import api_version
import tkinter.filedialog as fd
import tkinter as tk
from traceback import print_tb
from turtle import st
from urllib import request, response
from pytz_deprecation_shim import timezone
from setuptools import Command
import textract
import time
from threading import Thread
import datetime
import os.path
from collections import Counter
import matplotlib.pylab as plt
from datetime import timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload




#       Google kalendārs 

SCOPES = ['https://www.googleapis.com/auth/calendar']

# savienojums un pārbaude - nepieciešama pirmo reizi palaižot rīku
def Create_Service(client_secret_file, api_name, api_version, *scopes, prefix=''):
	CLIENT_SECRET_FILE = client_secret_file
	API_SERVICE_NAME = api_name
	API_VERSION = api_version
	SCOPES = [scope for scope in scopes[0]]
	
	cred = None
	working_dir = os.getcwd()
	token_dir = 'token files'
	pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

	### Check if token dir exists first, if not, create the folder
	if not os.path.exists(os.path.join(working_dir, token_dir)):
		os.mkdir(os.path.join(working_dir, token_dir))

	if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
		with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
			cred = pickle.load(token)

	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
			cred = flow.run_local_server()

		with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
			pickle.dump(cred, token)

	try:
		service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
		return service
	except Exception as e:
		print(e)
		print(f'Failed to create service instance for {API_SERVICE_NAME}')
		os.remove(os.path.join(working_dir, token_dir, pickle_file))
		return None





#       Google kalendārs 

# savienojums un pārbaude - nepieciešama pirmo reizi palaižot rīku


creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
#service = build('calendar', 'v3', credentials=creds)

service = Create_Service('credentials.json', 'Calendar', 'v3', SCOPES)


#       Google Drive

SCOPES2 = ['https://www.googleapis.com/auth/drive']

#service2 = build('drive', 'v3', credentials=creds)

try: 
    service2 = Create_Service('credentials.json', 'drive', 'v3', SCOPES2)

    # Call the Drive v3 API - Parbaude izvadot terminālā pirmos 10 dokumentus

#    results = service2.files().list(
#        pageSize=10, fields="nextPageToken, files(id, name, webViewLink)").execute()
#    items = results.get('files')
#
#    if not items:
#        print('No files found.')
#        
#    print('Files:')
#    for item in items:
#        print(u'{0} ({1}) {2}'.format(item['name'], item['id'], item['webViewLink']))

except HttpError as error:
    print(f'An error occurred: {error}')









#       Piemērs ar kalendāra izveidi !!!!!!!!!!!!!!!!
# Nepieciešams palaist tikai vienu reizi, lai izeidotu kalendāru ar jaunu nosaukumu

#request_body = {
#    'summary' : 'BD - PDF - Worst Case'
#}
#response = service.calendars().insert(body=request_body).execute()
#
#request_body = {
#    'summary' : 'BD - Word - Worst Case'
#}
#response = service.calendars().insert(body=request_body).execute()
#
#request_body = {
#    'summary' : 'BD - Photo - Worst Case'
#}
#response = service.calendars().insert(body=request_body).execute()
#
#request_body = {
#    'summary' : 'BD - Photo - Worst Case(Blur)'
#}
#response = service.calendars().insert(body=request_body).execute()
#

#       Izdrukā terminālā visus iespējamos kalendārus - var saprastu, kur tieši var ievietot
response = service.calendarList().list().execute()
response = response.get('items')
print("\n")
for x in response:
    print("Kalendāra nosaukums - ", x['summary'])
    print("Kalendāra ID - ", x['id'], "\n")



# ievietošana kalendārā
def ievadeKalendara(laiksIevade, datumsIevade, epastiIevade, dokumentaNosaukums, dokumentaCelsGoogleIevade):

    ct = datetime.datetime.now()
  

    # mainīgie priekš nosaukuma noteikšanas

    saiteUzID = saiteUzLietotni.get().strip()
    latvijaTime = '+03:00'

    radioPoga = radioPogasIzvele.get()
    nosaukumsIevadei = ["Lidojums", "Braukšana", "Viesnīca", "Brīvdienas"]
    nosaukumsSkaidrojums = ["Apraksta lidmašīnas veikto ceļošanas laiku", 
    "Apraksta ekipažas ceļošanu no vienas vietas līdz otrai", 
    "Apraksta to, cik ilgi noteiktajā viesnīcā ir palikusi ekipāža", 
    "Apraksta to, cik ilgas brīvdienas bija ekipāžai"]
    
    datumsPoga = datumsIzvele.get() # 1- izvēlēts, 0- neizvēlēts
    laiksPoga = laiksIzvele.get()
    epastsPoga = epastsIzvele.get()
    attelsPoga = attelsIzvele.get()

    # Izveido 2 mainīgos - 1-laiks un datums uz doto brīdi 2- pēc 1 stundas
    laiksUnDatums_s = datetime.datetime.now().isoformat()
    laiksUnDatums_b = datetime.datetime.now() + datetime.timedelta(hours = 1)
    laiksUnDatums_b = laiksUnDatums_b.isoformat()
    laiksUnDatums_s = str(laiksUnDatums_s)
    laiksUnDatums_b = str(laiksUnDatums_b)

    # Izveido 2 mainīgos - 1-datums uz doto brīdi 2- pēc 1 dienas
    datums_s = datetime.datetime.today().strftime('%Y-%m-%d')
    datums_b = datetime.datetime.today() + datetime.timedelta(days = 1)
    datums_s = str(datums_s)        # datums uz doto brīdi
    datums_b = str(datums_b)[:-16]  # datums pēc 1 dienas

    # Izveido 2 mainīgos - 1-laiks uz doto brīdi 2- pēc 1 stundas
    laiks_s = datetime.datetime.now().isoformat()
    laiks_b = datetime.datetime.today() + datetime.timedelta(hours = 1)
    laiks_s = str(laiks_s)[11:] # laiks uz doto brīdi
    laiks_b = str(laiks_b)[11:] # laiks pēc 1 stundas 

   
    # datumu un laiku savienošana
    
    # 1) Ir izvēlēts datums, ir izvēlēts laiks, ir 2 datumi, ir 2 laiki 
    if ((len(datumsIevade) == 2 ) and (len(laiksIevade) == 2) and (datumsPoga==1) and (laiksPoga==1)):
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiksIevade[0])
        beiguLaiks = str(datumsIevade[1] + "T"+ laiksIevade[1])
    # 2) Ir izvēlēts datums, ir izvēlēts laiks, ir 1 datums, ir 2 laiki    
    elif((len(datumsIevade) == 1 ) and (len(laiksIevade) >= 2) and (datumsPoga==1) and (laiksPoga==1)):
        laiksIevade.sort()
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiksIevade[0])
        beiguLaiks = str(datumsIevade[0] + "T"+ laiksIevade[1])
     # 3) Ir izvēlēts datums, ir izvēlēts laiks, ir 1 datums, ir 1 laiks    
    elif((len(datumsIevade) == 1 ) and (len(laiksIevade) == 1) and (datumsPoga==1) and (laiksPoga==1)):
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiksIevade[0])
        beiguLaiks = str(datumsIevade[0] + "T"+ laiksIevade[0])
        beiguLaiks = beiguLaiks[:-1]
        beiguLaiks = str(beiguLaiks+"1")
    # 4) Ir izvēlēts datums, ir izvēlēts laiks, ir 2 datumi, ir 1 laiks  
    elif((len(datumsIevade) >= 2 ) and (len(laiksIevade) == 1) and (datumsPoga==1) and (laiksPoga==1)):  
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiksIevade[0])
        beiguLaiks = str(datumsIevade[1] + "T"+ laiksIevade[0])
    # 5) Ir izvēlēts datums, nav izvēlēts laiks, ir 2 datumi 
    elif((len(datumsIevade) >= 2 ) and (datumsPoga==1) and (laiksPoga==0)):  
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiks_s)
        beiguLaiks = str(datumsIevade[1] + "T"+ laiks_b)
    # 6) Ir izvēlēts datums, nav izvēlēts laiks, ir 1 datums 
    elif((len(datumsIevade) == 1 ) and (datumsPoga==1) and (laiksPoga==0)): 
        sakumaLaiks = str(datumsIevade[0] + "T"+ laiks_s)
        beiguLaiks = str(datumsIevade[0] + "T"+ laiks_b)
    # 7) Nav izvēlēts datums, ir izvēlēts laiks, ir 2 laiki  
    elif((len(laiksIevade) >= 2) and (datumsPoga==0) and (laiksPoga==1)):
        laiksIevade.sort()
        sakumaLaiks = str(datums_s + "T"+ laiksIevade[0])
        beiguLaiks = str(datums_b + "T"+ laiksIevade[1])
    # 8) Nav izvēlēts datums, ir izvēlēts laiks, ir 1 laiks 
    elif((len(laiksIevade) == 1) and (datumsPoga==0) and (laiksPoga==1)):  
        sakumaLaiks = str(datums_s + "T"+ laiksIevade[0])
        beiguLaiks = str(datums_b + "T"+ laiksIevade[0])
        beiguLaiks = beiguLaiks[:-1]
        beiguLaiks = str(beiguLaiks+"1")
    # 9) Nav izvēlēts datums, Nav izvēlēts laiks 
    elif((datumsPoga==0) and (laiksPoga==0)):    
        sakumaLaiks = str(laiksUnDatums_s)
        beiguLaiks = str(laiksUnDatums_b)


    elif((len(datumsIevade) == 0 ) and (len(laiksIevade) == 2) and (datumsPoga==1) and (laiksPoga==1)):
        laiksIevade.sort()
        sakumaLaiks = str(datums_s + "T"+ laiksIevade[0])
        beiguLaiks = str(datums_s + "T"+ laiksIevade[1])
    elif((len(datumsIevade) == 0 ) and (len(laiksIevade) == 1) and (datumsPoga==1) and (laiksPoga==1)):
        sakumaLaiks = str(datums_s + "T"+ laiksIevade[0])
        beiguLaiks = str(datums_s + "T"+ laiksIevade[0])
        beiguLaiks = beiguLaiks[:-1]
        beiguLaiks = str(beiguLaiks+"1")


    else:
        sakumaLaiks = str(laiksUnDatums_s)
        beiguLaiks = str(laiksUnDatums_b)
        
    # notikuma īpašības
    if((epastsPoga==0) or (len(epastiIevade)==0) ):
        if attelsPoga == 1:
            event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attachments':[
                        {   
                            'fileUrl' : dokumentaCelsGoogleIevade,
                            'title' : 'Pielikums - attēls no dokumenta'
                        }
                    ]    
                    }
        else:
            event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },    
                    }

    else:
        if (len(epastiIevade)==1):
            if attelsPoga == 1:
                event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]}
                        ],
                        'attachments':[
                            {   
                            'fileUrl' : dokumentaCelsGoogleIevade,
                            'title' : 'Pielikums - attēls no dokumenta'
                            }
                        ]                    
                    }
            else:
                 event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]}
                        ],                   
                    }

        elif (len(epastiIevade)==2):
            if attelsPoga == 1:
                event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]},
                            {'email' : epastiIevade[1]}
                        ],
                        'attachments':[
                            {   
                            'fileUrl' : dokumentaCelsGoogleIevade,
                            'title' : 'Pielikums - attēls no dokumenta'
                            }
                        ]      
                    }
            else:
                event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]},
                            {'email' : epastiIevade[1]}
                        ],     
                    }

        else:
            if attelsPoga == 1:
                event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]},
                            {'email' : epastiIevade[1]},
                            {'email' : epastiIevade[2]}
                        ],
                        'attachments':[
                            {   
                            'fileUrl' : dokumentaCelsGoogleIevade,
                            'title' : 'Pielikums - attēls no dokumenta'
                            }
                        ]  
                    }
            else:
                event = {
                        'summary': nosaukumsIevadei[radioPoga],
                        'description': str(nosaukumsSkaidrojums[radioPoga] + "\n\nDokuments - " + dokumentaNosaukums),
                        'start': {
                            'dateTime': sakumaLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'end': {
                            'dateTime': beiguLaiks+latvijaTime,
                            'timeZone': 'Europe/Riga',
                        },
                        'attendees':[
                            {'email' : epastiIevade[0]},
                            {'email' : epastiIevade[1]},
                            {'email' : epastiIevade[2]}
                        ], 
                    }

    


    # ievade kalendārā !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        print("ievietošana google kalendārā\n")
        print(event)
        
        event = service.events().insert(calendarId=saiteUzID, body=event, supportsAttachments = True).execute() 


        ctb = datetime.datetime.now()
        ctm = ctb - ct
        print("Nepieciešamais laiks Ievadei:-", ctm)

    except HttpError as err:
            print(err)
            print("Kļūda ievadot vērtības kalendārā")



 

#   Izmēri un krāsas - mainigie
HEIGHT = 800
WIDTH = 1000
zils = '#E4EBF5'
dzeltens = '#F5F5D9'
gaisiSarkans = '#FFBCBC'
kosiSarkans = '#FF0000'
balts = '#FFFFFF'



pattern24h = re.compile(r'[ ](2[0-3]|[01]?[0-9])[:-]([0-5][0-9])[ ]') 

patternDate = re.compile(r'[0-9]{2}[-./][0-9]{2}[-./][0-9]{4}')
patternDate_2 = re.compile(r'[0-9]{4}[-./][0-9]{2}[-./][0-9]{2}')
patternDate_3 = re.compile(r'[0-9]{2}[-./][0-9]{4}[-./][0-9]{2}')

patternEpasts = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


#       Rīka funkcijas:

# Dokumentu izvēle un pievienošana sarakstam
def pievienot_failus():
    global izveletiDokumentiSaraksts # sarakst ar visu ceļu
    global izveletiDokumentiSarakstsIss  # sarakst ar dokumentu nosaukumiem
    global dokumentuSkaits

    global datumsG
    global laiksG
    global epastsG
    
    datumsG = []
    laiksG = []
    epastsG = []

    izveletiDokumentiSaraksts = [] 
    izveletiDokumentiSarakstsIss = []

    sarakstsDokumentu.delete(0, "end")


    izveletiDokumenti = fd.askopenfilenames(parent=root, title='Izvēlaties dokumentus, kurus vēlaties pievienot:', filetypes=[("Visi Dokumenti", "*.docx *.pdf *.png *.jpeg *.jpg"), ("Attēli", "*.png *.jpeg *.jpg"), ("Word", "*.docx *.doc"), ("PDF", "*.pdf")])
    izveletiDokumentiSaraksts= root.tk.splitlist(izveletiDokumenti)

    #print(izveletiDokumentiSaraksts) # sarakst ar visu ceļu

    for x in izveletiDokumentiSaraksts:
        head_path, tail_path = os.path.split(x)
        izveletiDokumentiSarakstsIss.append(tail_path)
        sarakstsDokumentu.insert("end", tail_path) # lietotājam redzams saraksts

    #print(izveletiDokumentiSarakstsIss) # sarakst ar dokumentu nosaukumiem

    dokumentuSkaits = len(izveletiDokumentiSarakstsIss) # dokumentu skaits sarakstā
    dokumentsTekstsArSkaitu = ("Izēlēto dokumentu skaits = {}").format(dokumentuSkaits)
    aprakstsSkaits.config(text = dokumentsTekstsArSkaitu) # dokumentu skaita izvade lietotājam

    aprakstsSkaitsPaveikts.config(text= ("{} / {}").format(0,dokumentuSkaits) )


    print("Izvēlētu dokumentu skaits - ", dokumentuSkaits)

    if dokumentuSkaits>0:
        sarakstsDokumentu.config( bg=balts)
    else:
        sarakstsDokumentu.config( bg=gaisiSarkans)

    


# Funkcija atļauj pārtraukt darbu, kamēr notiek process
def start_tryout():
    Thread(target=ievietot_failus, daemon=True).start()

def start_tryout_2():
    Thread(target=uzsaktDarbu, daemon=True).start()

def uzsaktDarbu():
    global darbs 
    darbs = True

def parTrauktDarbu():
    global darbs 
    darbs = False



# Dokumentu nolasīšana no saraksta
def ievietot_failus():

    ct = datetime.datetime.now()
    print("Sakums:-", ct)

    skaits = 1

    if(len(saiteUzLietotni.get())>0):
     
        for x in izveletiDokumentiSaraksts:
            print("\n\nDokuments nr -", skaits, "\tDokumenta nosaukums -", izveletiDokumentiSarakstsIss[skaits-1])  
           
            if darbs:


                cp = datetime.datetime.now()


                teksts = textract.process(x) 


                cte = datetime.datetime.now()
                cmp = cte - cp
                print("Nepieciešamais laiks teksta parsēšanai:-", cmp)



                tekstaAnalize(teksts, izveletiDokumentiSarakstsIss[skaits-1], x)
                time.sleep(0.08)
                aprakstsSkaitsPaveikts.after(50, izmainitSkaitli, skaits)

                #print(saiteUzLietotni.get(), "\n" )
            else:
                while darbs == False:
                    time.sleep(1)
            skaits += 1

        
        ctb = datetime.datetime.now()
        print("\nBeigas:-", ctb)

        ctm = ctb - ct
        print("Sakums:-", ct)
        print("Nepieciešamais laiks:-", ctm)
        print("E-pasts netika atrasts:-", kludasEpasts, "reizes, dokumentos: ", kludasEpastsList)
        print("Datums netika atrasts:-", kludasDatums, "reizes, dokumentos: ", kludasDatumsList)
        print("Laiks netika atrasts:-", kludasLaiks, "reizes, dokumentos: ", kludasLaiksList)

        response = service.calendarList().list().execute()
        response = response.get('items')
        print("\n")
        for x in response:
            print("Kalendāra nosaukums - ", x['summary'])
            print("Kalendāra ID - ", x['id'], "\n")



        #   Grafiskais attēlojums

#        if datumsIzvele.get() == 1:
#            datumsG.sort()
#            countD ={}
#            for i in datumsG:
#                if not i in countD:
#                    countD[i] = 1
#                else:
#                    countD[i] += 1
#            lists = sorted(countD.items())
#            x, y = zip(*lists)
#            plt.plot(x, y)
#            plt.show()
#
#
#
#        if laiksIzvele.get() == 1:
#            laiksG.sort()
#            countL ={}
#            for i in laiksG:
#                if not i in countL:
#                    countL[i] = 1
#                else:
#                    countL[i] += 1
#            lists = sorted(countL.items())
#            x, y = zip(*lists) 
#            plt.plot(x, y)
#            plt.show()
#
#        if epastsIzvele.get() == 1:
#            epastsG.sort()
#            countE ={}
#            for i in epastsG:
#                if not i in countE:
#                    countE[i] = 1
#                else:
#                    countE[i] += 1
#            lists = sorted(countE.items()) 
#            x, y = zip(*lists) 
#            plt.plot(x, y)
#            plt.show()
#

        


    else:
        print("\nNav ievadīts tekst ievades laukā 'Lietotnes saite' ID")

   



# dokumentu skaitišana
def izmainitSkaitli(skaits):
    aprakstsSkaitsPaveikts.config(text= ("{} / {}").format(skaits,dokumentuSkaits) )


kludasEpasts = 0
kludasLaiks = 0
kludasDatums = 0
kludasEpastsList = []
kludasLaiksList = []
kludasDatumsList = []

# Noteiktu mainīgo noteikšana no teksta
def tekstaAnalize(tekstsAnalize, dokumentaNosaukums, saiteUzDokumentu):

    ct = datetime.datetime.now()
    
    radioPogaA = radioPogasIzvele.get()
    dienas = [40, 50, 60, 70]

    global kludasEpasts
    global kludasLaiks
    global kludasDatums
    global kludasEpastsList
    global kludasLaiksList
    global kludasDatumsList
   
      
    datumsPoga2 = datumsIzvele.get() # 1- izvēlēts, 0- neizvēlēts
    laiksPoga2 = laiksIzvele.get()
    epastsPoga2 = epastsIzvele.get()
    attelsPoga2 = attelsIzvele.get()
    

    dokumentaNosaukums = dokumentaNosaukums
    datumiJauni = []
    laikiJauni = []
    epsatiJauni = []
    atrastsEpastsDict ={}
    atrastiEpasts = []
    dokumentaCelsGoogle = ""


    tekstsRinda = str(tekstsAnalize)

    # Lieku rindu aizvietošana      
    tekstsRinda = tekstsRinda.replace(r"\n", " ")
    tekstsRinda = tekstsRinda.replace(r"\t", " ")
    tekstsRinda = tekstsRinda.replace(r"\r", " ")
    
    # teksta izvadīšana no dokumenta
    print("Teksts dokumentā:\n",tekstsRinda, "\n")
   

    # Laika pārbaude
    if laiksPoga2 == 1:
        try:
            atrastsLaiks = pattern24h.findall(tekstsRinda)
            for x in atrastsLaiks:
                laiks24 = str(x[0] + ":" + x[1] + ":00")
                laikiJauni.append(laiks24)
                laiksG.append(laiks24)
                
        except:
            print("\nNeizdevās atrast laiku")

    if laiksPoga2 == 1 and len(laikiJauni) == 0:
        kludasLaiks = kludasLaiks + 1
        kludasLaiksList.append(dokumentaNosaukums)
        


    # Datuma pārbaude 
    if datumsPoga2 == 1:
        try:

            atrastsDatums = patternDate.findall(tekstsRinda)
            atrastsDatums.extend(patternDate_2.findall(tekstsRinda))
            atrastsDatums.extend(patternDate_3.findall(tekstsRinda))

            for x in atrastsDatums:  
                dat = str(x)

                dat = dat.replace(".", "-")
                dat = dat.replace("/", "-")
                
                try:
                    e = datetime.datetime.strptime(dat, "%d-%m-%Y").strftime("%Y-%m-%d")
                    datumiJauni.append(e)
                except:
                    try:
                        e = datetime.datetime.strptime(dat, "%m-%d-%Y").strftime("%Y-%m-%d")
                        datumiJauni.append(e)
                    except:
                        try:
                            e = datetime.datetime.strptime(dat, "%Y-%m-%d").strftime("%Y-%m-%d")
                            datumiJauni.append(e)
                        except:
                            try:
                                e = datetime.datetime.strptime(dat, "%Y-%d-%m").strftime("%Y-%m-%d")
                                datumiJauni.append(e)
                            except:
                                try:
                                    e = datetime.datetime.strptime(dat, "%m-%Y-%d").strftime("%Y-%m-%d")
                                    datumiJauni.append(e)
                                except:
                                    try:
                                        e = datetime.datetime.strptime(dat, "%d-%Y-%m").strftime("%Y-%m-%d")
                                        datumiJauni.append(e)
                                    except:
                                        print("Nepareizs datuma formāts")  


            datumsG.append(e)
            datumiJauni.sort()

        except:
            kludasDatums = kludasDatums + 1
            print("\nNeizdevās atrast datumu") 

    if datumsPoga2 == 1 and len(datumiJauni) == 0:
        kludasDatums = kludasDatums + 1
        
        
        kludasDatumsList.append(dokumentaNosaukums)



 # E-pastu pārbaude
    if epastsPoga2 == 1:
        try:
            atrastiEpasts = patternEpasts.findall(tekstsRinda)
            atrastiEpasts = list(dict.fromkeys(atrastiEpasts))

            for x in atrastiEpasts:
                #atrastsEpastsDict['email'] = {'email:',x}
                #epsatiJauni.append((atrastsEpastsDict['email']))  
                epsatiJauni.append(x)
                epastsG.append(x)
        except:
            print("\nNeizdevās atrast e-pastu") 

    if epastsPoga2 == 1 and len(epsatiJauni) == 0:
        kludasEpasts = kludasEpasts + 1
        kludasEpastsList.append(dokumentaNosaukums)
    






    if attelsPoga2 == 1:
        name, extension = os.path.splitext(saiteUzDokumentu)
        dokumentaCels = ""

        if extension == '.docx':
            
            doc = aw.Document(saiteUzDokumentu)
           
            shapes = doc.get_child_nodes(aw.NodeType.SHAPE, True)
            imageIndex = 0
            
            for shape in shapes :
                shape = shape.as_shape()
                if (shape.has_image) :
                  
                    imageFileName = (name + f".png")
                    
                    shape.image_data.save(imageFileName)
                    dokumentaCels = str(name + f".png")
                    break
                break

        if extension == '.pdf':
           
            pdf_file = fitz.open(saiteUzDokumentu)
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                image_list = page.getImageList()
                for image_index, img in enumerate(page.getImageList(), start=1):
                    xref = img[0]
                    base_image = pdf_file.extractImage(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(open(name + ".png", "wb"))
                    dokumentaCels = str(name + f".png")

        if extension == '.png' or extension == '.jpg' or extension == '.jpeg':
            dokumentaCels = str(name + f".png")

        if dokumentaCels != "":
            file_metadata = {'name': 'Attels_no_dokumenta.png'}
            media = MediaFileUpload(dokumentaCels, mimetype='image/png')
            saglabatsAttels = service2.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()
            print ('File ID: %s' % saglabatsAttels.get('webViewLink'))
            dokumentaCelsGoogle = saglabatsAttels.get('webViewLink')




    ievade = 0
    beigt = 0
    if len(datumiJauni)>=3:
        while beigt == 0:
            deltaS = datetime.datetime.strptime(datumiJauni[1], "%Y-%m-%d") - datetime.datetime.strptime(datumiJauni[0], "%Y-%m-%d")
            deltaB = datetime.datetime.strptime(datumiJauni[-1], "%Y-%m-%d") - datetime.datetime.strptime(datumiJauni[-2], "%Y-%m-%d")
            if deltaS > timedelta(days=dienas[radioPogaA]):
                datumiJauni.pop(0)
            elif deltaB > timedelta(days=dienas[radioPogaA]):
                datumiJauni.pop()
            else:
                beigt = 1

    if len(datumiJauni) % 2 == 1:
        deltaS = datetime.datetime.strptime(datumiJauni[1], "%Y-%m-%d") - datetime.datetime.strptime(datumiJauni[0], "%Y-%m-%d")
        deltaB = datetime.datetime.strptime(datumiJauni[-1], "%Y-%m-%d") - datetime.datetime.strptime(datumiJauni[-2], "%Y-%m-%d")
        if deltaS > deltaB:
            datumiJauni.pop(0)
        else:
            datumiJauni.pop()


    if len(datumiJauni) >= len(laikiJauni):
        for x in range(0, len(datumiJauni), 2):
            datumsK = []
            laiksK = []
            try:
                datumsK.append(datumiJauni[x])
            except:
                pass
            try:
                datumsK.append(datumiJauni[x+1])
            except:
                pass

            try:
                laiksK.append(laikiJauni[x])
            except:
                pass
            try:
                laiksK.append(laikiJauni[x+1])
            except:
                pass
            ievade = 1
            ievadeKalendara(laiksK, datumsK, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle)  

    elif len(datumiJauni) == 0:
        for x in range(0, len(laikiJauni), 2):
            laiksK = []
            try:
                laiksK.append(laikiJauni[x])
            except:
                pass
            try:
                laiksK.append(laikiJauni[x+1])
            except:
                pass
            ievade = 1
            ievadeKalendara(laiksK, datumiJauni, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle)  

    elif len(laikiJauni) == 0:
        for x in range(0, len(datumiJauni), 2):
            datumsK = []
            try:
                datumsK.append(datumiJauni[x])
            except:
                pass
            try:
                datumsK.append(datumiJauni[x+1])
            except:
                pass
            ievade = 1
            ievadeKalendara(laikiJauni, datumsK, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle) 
    

    elif len(laikiJauni) == 0 and len(datumiJauni) == 0:
        ievade = 1
        ievadeKalendara(laikiJauni, datumiJauni, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle)




    else:
        for x in range(0, len(laikiJauni), 2):
            datumsK = []
            laiksK = []
            try:
                datumsK.append(datumiJauni[x])
            except:
                pass
            try:
                datumsK.append(datumiJauni[x+1])
            except:
                pass

            try:
                laiksK.append(laikiJauni[x])
            except:
                pass
            try:
                laiksK.append(laikiJauni[x+1])
            except:
                pass
            ievade = 1
            ievadeKalendara(laiksK, datumsK, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle)

    if ievade == 0:
        ievadeKalendara(laikiJauni, datumiJauni, epsatiJauni, dokumentaNosaukums, dokumentaCelsGoogle)



    ctb = datetime.datetime.now()
    ctm = ctb - ct
    print("Nepieciešamais laiks Analīzei:-", ctm)
    

    






# Krasa saitei uz lietotni
def krasaSaite(*args):
    if(len(saiteUzLietotni.get())>0):
        saiteIevade.config(bg=balts)
    else:
        saiteIevade.config(bg=gaisiSarkans)

    




#       Rīka GUI - nepieciesams, lai rīkam būtu grafiskais interfeiss

root = tk.Tk()

root.title("Riks automatizetai ievadei")
root.geometry("+750+300") # vieta, kurā rīks atversies (x un y no ekrāna izmēra)

#       Rīka izmēri
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = zils)
frame.place(relheight=1, relwidth=1)


#       Rīka aprakstošie teksti

# Rīka pilnais nosaukums
virsraksts = tk.Label(frame, text="RĪKS AUTOMATIZĒTAI DOKUMENTU PARSĒŠANAI,\n\tIEGŪTO DATU ANALĪZEI UN IEVADEI", justify='left',  font=('Times New Roman', 22 ),bg = zils)
virsraksts.place(relheight=0.2, relwidth=0.8, relx=0.1, rely=0.02)

# teksts virs saraksta
aprakstsSaraksts = tk.Label(frame, text="PIEVIENOTIE DOKUMENTI",bg = zils, fg='black', font=('Times New Roman', 9 ))
aprakstsSaraksts.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.2)

# teksts zem saraksta - dokumentu skaits
aprakstsSkaits = tk.Label(frame, text="Izēlēto dokumentu skaits = 0",bg = zils, fg='black', font=('Times New Roman', 9 ))
aprakstsSkaits.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.65)

# teksts virs saites uz lietotne
aprakstsSaite = tk.Label(frame, text="IZVĒLĒTĀS LIETOTNES ID",bg = zils, fg='black', font=('Times New Roman', 9 ))
aprakstsSaite.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0.2)

# teksts zem pogas VEIKT DATU IEVADI - parāda to cik daudz dokumentu jau ir ievadīti no kopējā saraksta
aprakstsSkaitsPaveikts = tk.Label(frame, text="0 / 0",bg = zils, fg='black', font=('Times New Roman', 9 ))
aprakstsSkaitsPaveikts.place(relheight=0.05, relwidth=0.2, relx=0.7, rely=0.85)




#       Pogas rīkā

# Pievienot datus
pievienotDatus = tk.Button(frame, text="PIEVIENOT DATUS", bg= dzeltens, fg='black', font=('Times New Roman', 13 ),borderwidth=3, relief = tk.RIDGE, command=lambda:pievienot_failus())
pievienotDatus.place(relheight=0.1, relwidth=0.30, relx=0.05, rely=0.75)

# Veikt datu ievadi
ievaditDatus = tk.Button(frame, text="VEIKT DATU IEVADI", bg= dzeltens, fg='black', font=('Times New Roman', 13 ),borderwidth=3, relief = tk.RIDGE, command=lambda:[uzsaktDarbu(),start_tryout()] )
ievaditDatus.place(relheight=0.1, relwidth=0.30, relx=0.65, rely=0.75)

# Aizvērt rīku
aizvert = tk.Button(frame, bg = zils, fg = kosiSarkans, text = "AIZVĒRT", font=('Times New Roman', 13 ), borderwidth = 0, command = lambda: zinojumsPirmsAizversanas() )
aizvert.place(relheight=0.1, relwidth=0.1, relx=0.9, rely=0.9)

# Pārtraukt darbu
aizvert = tk.Button(frame, bg = zils, fg = kosiSarkans, text = "PĀRTRAUKT DARBU", font=('Times New Roman', 13 ), borderwidth = 0, command = lambda: parTrauktDarbu() )
aizvert.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.9)

# Turpināt darbu
aizvert = tk.Button(frame, bg = zils, fg = kosiSarkans, text = "TURPINĀT DARBU", font=('Times New Roman', 13 ), borderwidth = 0, command = lambda: start_tryout_2() )
aizvert.place(relheight=0.1, relwidth=0.15, relx=0.55, rely=0.9)



#       Saraksti rīkā

# Saraksts ar izvēlētiem dokumentiem
sarakstsDokumentu = tk.Listbox(frame, bg=gaisiSarkans, font=('Times New Roman', 13))
sarakstsDokumentu.place(relheight=0.4, relwidth=0.4, relx=0.05, rely=0.25)


#       Ievades lauki rīkā

# Saite uz lietotni
saiteUzLietotni = tk.StringVar()
saiteUzLietotni.trace('w',krasaSaite)
saiteIevade = tk.Entry(frame, font=('Times New Roman', 13 ), bg=gaisiSarkans, textvariable=saiteUzLietotni )
saiteIevade.place(relheight=0.05, relwidth=0.45, relx=0.5, rely=0.25)



#       Radio un izvēles pogas

# mainīgie
datumsIzvele = tk.IntVar()
laiksIzvele = tk.IntVar()
epastsIzvele = tk.IntVar()
attelsIzvele = tk.IntVar()

# pirmais sarkasts - izvēles pogas
c1 = tk.Checkbutton(frame, text = "Datums", bg=zils, font=('Times New Roman', 13 ), variable = datumsIzvele, onvalue=1, offvalue=0 )
c1.place(relheight=0.05, relwidth=0.1, relx=0.49, rely=0.35)
c1.select()

c2 = tk.Checkbutton(frame, text = "Laiks", bg=zils, font=('Times New Roman', 13 ), variable = laiksIzvele, onvalue=1, offvalue=0 )
c2.place(relheight=0.05, relwidth=0.1, relx=0.484, rely=0.4)
c2.select()

c3 = tk.Checkbutton(frame, text = "E-pasts", bg=zils, font=('Times New Roman', 13 ), variable = epastsIzvele, onvalue=1, offvalue=0 )
c3.place(relheight=0.05, relwidth=0.1, relx=0.49, rely=0.45)

c4 = tk.Checkbutton(frame, text = "Attēli", bg=zils, font=('Times New Roman', 13 ), variable = attelsIzvele, onvalue=1, offvalue=0 )
c4.place(relheight=0.05, relwidth=0.1, relx=0.486, rely=0.5)


# otrais saraksts
radioPogasIzvele = tk.IntVar() 
r1 = tk.Radiobutton(frame, text = "Lidojums", bg=zils, font=('Times New Roman', 13 ), variable = radioPogasIzvele, value=0)
r1.place(relheight=0.05, relwidth=0.1, relx=0.70, rely=0.35)

r2 = tk.Radiobutton(frame, text = "Braukšana", bg=zils, font=('Times New Roman', 13 ), variable = radioPogasIzvele, value=1)
r2.place(relheight=0.05, relwidth=0.1, relx=0.702, rely=0.4)

r3 = tk.Radiobutton(frame, text = "Viesnīca", bg=zils, font=('Times New Roman', 13 ), variable = radioPogasIzvele, value=2)
r3.place(relheight=0.05, relwidth=0.1, relx=0.698, rely=0.45)

r4 = tk.Radiobutton(frame, text = "Brīvdienas", bg=zils, font=('Times New Roman', 13 ), variable = radioPogasIzvele, value=3)
r4.place(relheight=0.05, relwidth=0.1, relx=0.704, rely=0.5)


#       Ziņojuma logs pirms rīka aizvēršanas

def zinojumsPirmsAizversanas():
    # ziņojuma izveidošana
    zinojums = tk.Tk()
    zinojums.grab_set_global()
    zinojums.geometry("+1100+500")
    # ziņojuma nosaukums
    zinojums.title("Aizvērt rīku?")
    canvasZinojums = tk.Canvas(zinojums, height=300, width=400)
    canvasZinojums.pack()
    
    # pamats ziņojumam
    frameZinojums = tk.Frame(zinojums, bg = zils, highlightbackground="black", highlightthickness=1)
    frameZinojums.place(relheight=1, relwidth=1)

    frameLinija= tk.Frame(zinojums, bg = "black")
    frameLinija.place(relheight=0.0005, relwidth=1, relx=0, rely=0.77)
    
    # pogas - neaizvērt rīku
    zinojumsNe = tk.Button(frameZinojums, text="Nē", bg= zils, fg='black', font=('Times New Roman', 13 ),borderwidth=3, relief = tk.RIDGE, command = zinojums.destroy)
    zinojumsNe.place(relheight=0.1, relwidth=0.30, relx=0.05, rely=0.83)
    # pogas - aizvērt rīku
    zinojumsAizvert = tk.Button(frameZinojums, text="Aizvērt", bg= kosiSarkans, fg=balts, font=('Times New Roman', 13 ),borderwidth=3, relief = tk.RIDGE, command = exit)
    zinojumsAizvert.place(relheight=0.1, relwidth=0.30, relx=0.65, rely=0.83)

    # Paskaidrojošais teksts
    virsraksts = tk.Label(frameZinojums, text="Darbības, kuras Jūs veicat tiks\n pārtauktas", justify='center',  font=('Times New Roman', 18 ),bg = zils)
    virsraksts.place(relheight=0.3, relwidth=0.75, relx=0.15, rely=0.2)
    # Paskaidrojošais teksts

    virsraksts = tk.Label(frameZinojums, text="Jūs tiešām vēlaties aizvērt rīku?", justify='center',  font=('Times New Roman', 11 ),bg = zils)
    virsraksts.place(relheight=0.05, relwidth=0.7, relx=0.15, rely=0.7)
    
# Funkcija, kura nodrosina to, lai rika grafiskais interfeiss neaizveras pirms to velas lietotajs
root.mainloop()