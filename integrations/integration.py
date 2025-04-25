import json
import requests
import traceback
from decouple import config as load_data
from integrations.models import (
    insert_integraciones_sinc
    , update_integraciones_sinc
    , time_zone
    , response_gs_objects
    , get_data_integraciones_sinc
)
from lib.Stech import Logger, Stech
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class Integration():

    @classmethod
    def get_points(self):
        try:

            data_timezone = time_zone()
            if not data_timezone:
                raise ValueError("Error al obtener la zona horaria")

            query_results = response_gs_objects(data_timezone, load_data('USER_ID'))
            if not query_results:
                raise ValueError("Error al obtener los datos de la consulta")

            url = "https://apiv2.gausscontrol.com/v2/processor/events/positionupdate/upload"
            payload = json.dumps(query_results)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlc1Blcm1pc3Npb25zIjpbeyJyb2xlTmFtZSI6IkFwaUluamVjdGlvbiIsInBlcm1pc3Npb25zIjpbXX1dLCJ1c2VyX25hbWUiOiJ0ZXN0QGJsYWNrYXkuY29tIiwibGFuZ3VhZ2UiOiJlcyIsImxpbmtlZFBlb3BsZUlkIjpudWxsLCJ1c2VyTmFtZSI6InRlc3RAYmxhY2theS5jb20iLCJ1c2VySWQiOjE2MzI1LCJhdXRob3JpdGllcyI6WyJBcGlJbmplY3Rpb24iXSwiY2xpZW50X2lkIjoiZ2F1c3Njb250cm9sYXBpIiwiYXVkIjpbInRlc3Rqd3RyZXNvdXJjZWlkIl0sInZpZXdlZFRvdXJzIjpbXSwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sInJvb3QiOmZhbHNlLCJuYW1lIjoiQmxhY2theSIsInRlbmFudElkIjoidGVzdGluZyIsImxpbmtlZFBlb3BsZUNvZGUiOm51bGwsIkxpbmtlZFBlb3BsZVRhZ3MiOltdLCJleHAiOjI2OTIyNTYzNTksInRhZ3NQZXJtaXNzaW9ucyI6W3sidGFnIjoiKiIsInRhZ0NhdGVnb3J5IjoiQ0FSUklFUiJ9LHsidGFnIjoiKiIsInRhZ0NhdGVnb3J5IjoiRFNfQ0FSUklFUiJ9XSwiZmlsdGVyVGFncyI6e30sImp0aSI6ImRiNjM5OTExLTY2YTMtNDEzZS04ZmViLTBkZmYwMzY5ZDQ3MiJ9.AWuY27m1yLF0uZVao48iYtx79zXXR96JxOdFlkfcHyc'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                #code_response = json.loads(response.json())
                print(response.text)
                data_log = {
                    "imei": query_results[0]['vehicleCode'],
                    "response": response.text,
                    "status_code": response.status_code
                }
                Logger.add_to_log("success", str(data_log), load_data('LOG_DIRECTORY'), "log_success_dgm")
                    
        except ValueError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_error_dgm")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_error_dgm")
        
        except SQLAlchemyError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_error_dgm")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_error_dgm")

        except Exception as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_error_dgm")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_error_dgm")
