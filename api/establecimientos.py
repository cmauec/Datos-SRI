#!/usr/bin/env python
#
# Copyright 2016  Carlos Vaca 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import logging
import json
import cgi
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from apiclient import errors
import httplib2
import cloudstorage as gcs
from google.appengine.api import app_identity

# Comprobar si estamos en el servidor de desarrollo o produccion
debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

# Para pruebas en el servidor de desarrollo
if debug:
    with open("config.json", "r") as myfile:
        config = json.loads(myfile.read())
    with open("secret.pem") as f:
        private_key = f.read()
else: 
    # Direccion del bucket por defecto del proyecto, para crearlo hacerlo en https://appengine.google.com
    bucket = '/' + app_identity.get_default_gcs_bucket_name()

    # Cargamos el archivo con los datos de configuracion
    file_config = bucket+'/config.json'
    gcs_file_config = gcs.open(file_config)
    config = json.loads(gcs_file_config.read())

    # Cargamos el archivo con la clave privada para conectarnos a las Apis de Google
    # Con el archivo .p12 que nos bajamos de la consola de Google Cloud no funciona en el servidor de desarrollo, hay que pasarlo a .pem
    file_secret = bucket+'/secret.pem'
    gcs_file_secret = gcs.open(file_secret)
    private_key = gcs_file_secret.read()

client_email = config['client_email']
DATA_PROJECT_ID = config['DATA_PROJECT_ID']
DATASET = config['DATASET']
TABLE = config['TABLE']
api = config['API']

credentials = SignedJwtAssertionCredentials(client_email,private_key,api)
http = credentials.authorize(httplib2.Http())
bigquery_service = build("bigquery", "v2", http=http)


class Establecimientoshandler(webapp2.RequestHandler):
    def get(self):
        year_from = cgi.escape(self.request.get('from'))
        year_to = cgi.escape(self.request.get('to'))
        total = cgi.escape(self.request.get('total'))
        try:
            int(year_from),int(year_to)
        except:
            self.response.write('not-data')
            return
        if int(year_to) < int(year_from):
            self.response.write('not-data')
            return
        if total == '1':
            QUERY ='''
            SELECT
              count(*)
            FROM
              [Negocios.Lista]
            WHERE
              year(FECHA_INICIO_ACTIVIDADES) >= {0} and year(FECHA_INICIO_ACTIVIDADES) <= {1}
        '''.format(year_from,year_to)
        else:
            QUERY ='''
                SELECT
                  year(FECHA_INICIO_ACTIVIDADES) as FECHA_INICIO_ACTIVIDADES,
                  count(FECHA_INICIO_ACTIVIDADES) as total
                FROM
                  [Negocios.Lista]
                WHERE
                  year(FECHA_INICIO_ACTIVIDADES) >= {0} and year(FECHA_INICIO_ACTIVIDADES) <= {1}
                GROUP BY
                  FECHA_INICIO_ACTIVIDADES
                order by
                   FECHA_INICIO_ACTIVIDADES asc
            '''.format(year_from,year_to)
        query_config = {
            'query': QUERY,
            'timeoutMs': 10000
        }
        jobs = bigquery_service.jobs().query(projectId=DATA_PROJECT_ID,body=query_config).execute(http)
        data = []
        try:
            for i in jobs['rows']:
                data.append({'year':i['f'][0]['v'],"total":i['f'][1]['v']})
        except:
            self.response.write('not-data')
            return
        result = {'schema':['year','total'],'data':data}
        # self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))

app = webapp2.WSGIApplication([
    ('/api/establecimientos', Establecimientoshandler)
], debug=debug)
