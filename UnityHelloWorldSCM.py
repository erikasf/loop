# for python 2.x, import httplib and urlparse instead of httplib and urlparse 
import json
import httplib
import urlparse
import sys

# change these to your server and credentials
Url = 'http://sunriselatestga.unitysandbox.com'
Svc_username = 'Medlo-0f38-medlooprx-test'
Svc_password = 'M%fL!dPrxM%2L!3PrxT%sTbpPc1197'

Appname      = 'MedloopRx.medlooprx.TestApp'

Ehr_username = 'james'
Ehr_password = 'Password#1'

# *******************************************************************************************************
# * NAME:        UnityHelloWorldSCM.py
# *
# * DESCRIPTION: Example Python application code to illustrate basic usage of Unity with Allscripts
# *              Sunrise Clinical Manager (SCM).
# *
# * Unpublished (c) 2014 Allscripts Healthcare Solutions, Inc. and/or its affiliates. All Rights Reserved.
# *
# * This software has been provided pursuant to a License Agreement, with Allscripts Healthcare Solutions,
# * Inc. and/or its affiliates, containing restrictions on its use. This software contains valuable trade
# * secrets and proprietary information of Allscripts Healthcare Solutions, Inc. and/or its affiliates
# * and is protected by trade secret and copyright law. This software may not be copied or distributed
# * in any form or medium, disclosed to any third parties, or used in any manner not provided for in
# * said License Agreement except with prior written authorization from Allscripts Healthcare Solutions,
# * Inc. and/or its affiliates. Notice to U.S. Government Users: This software is "Commercial Computer
# * Software."
# *
# * This is example code, not meant for production use.
# *******************************************************************************************************


# build Magic action JSON string
def buildjson(action, appname, ehruserid, patientid, unitytoken,
              param1='', param2='', param3='', param4='', param5='', param6='', data='null'):
    return json.dumps({'Action': action,
                       'Appname': appname,
                       'AppUserID': ehruserid,
                       'PatientID': patientid,
                       'Token': unitytoken,
                       'Parameter1': param1, 'Parameter2': param2, 'Parameter3': param3,
                       'Parameter4': param4, 'Parameter5': param5, 'Parameter6': param6,
                       'Data': data})

# post action JSON to MagicJson endpoint, get JSON in return
def unityaction(jsonstr):
    u = urlparse.urlparse(Url)
    
    if (u.scheme == 'http'):
        conn = httplib.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = httplib.HTTPSConnection(u.hostname)

    conn.request('POST', '/Unity/UnityService.svc/json/MagicJson',
             jsonstr,
             {'Content-Type': 'application/json'})
    resp = conn.getresponse( )
    retjson = resp.read( ).decode( )
    conn.close( )
    return retjson

# get Unity security token from GetToken endpoint
def gettoken(username, password):
    u = urlparse.urlparse(Url)
    
    if (u.scheme == 'http'):
        conn = httplib.HTTPConnection(u.hostname)
    elif (u.scheme == 'https'):
        conn = httplib.HTTPSConnection(u.hostname)
    
    conn.request('POST', '/Unity/UnityService.svc/json/GetToken',
             json.dumps({'Username': username, 'Password': password}),
             {'Content-Type': 'application/json'})
    response = conn.getresponse( )
    t = response.read( ).decode( )
    conn.close( )
    return t

# Get Unity security token
token = gettoken(Svc_username, Svc_password)
print('Using Unity security token: ' + token)

# Authenticate Sunrise user before calling Magic actions
jsonstr = buildjson('GetUserAuthentication', Appname, Ehr_username, '', token, Ehr_password)
unity_output = unityaction(jsonstr)

print('Output from GetUserAuthentication: ')
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

# Call GetServerInfo Magic action; patient ID, Parameter1-6, and data not used
jsonstr = buildjson('GetServerInfo', Appname, Ehr_username, '', token)
unity_output = unityaction(jsonstr)

print('Output from GetServerInfo: ')
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

# Call GetPatient Magic action; Parameter1-6 and data not used in this example
patient = input('Enter a Patient ID to display (e.g., 5200200): ')
if patient.strip( ) == '':
    print('No patient ID specified; exiting.')
    sys.exit(0)
jsonstr = buildjson('GetPatient', Appname, Ehr_username, patient, token)
unity_output = unityaction(jsonstr)

print('Output from GetPatient: ')
print(json.dumps(json.loads(unity_output), indent=4, separators=(',', ': ')))

# python -m SimpleHTTPServer 8000
# static.issu.com/webembed/viewers/style1/v2/IssuuReader
