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
import jinja2
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
else: 
    # Direccion del bucket por defecto del proyecto, para crearlo hacerlo en https://appengine.google.com
    bucket = '/' + app_identity.get_default_gcs_bucket_name()

    # Cargamos el archivo con los datos de configuracion
    file_config = bucket+'/config.json'
    gcs_file_config = gcs.open(file_config)
    config = json.loads(gcs_file_config.read())


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values={
            'ID_ANALYTICS':config['ID_ANALYTICS']
        }
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
        template = jinja_environment.get_template('view/index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=debug)
