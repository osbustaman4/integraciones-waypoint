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
from lib.Stech import Logger
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class Waypoint():

    @classmethod
    def integration_wp_01(self):
        try:

            data_timezone = time_zone()
            if not data_timezone:
                raise ValueError("Error al obtener la zona horaria")

            query_results = response_gs_objects(data_timezone, 1)
            if not query_results:
                raise ValueError("Error al obtener los datos de la consulta")

            for query in query_results:

                if query.nsat > 3:
                    
                    payload = [
                                {
                                    "fecha": query.fecha,
                                    "latitud": query.latitud,
                                    "longitud": query.longitud,
                                    "altitud": query.altitud,
                                    "velocidad": query.velocidad,
                                    "cog": query.cog,
                                    "nsat": query.nsat,
                                    "realtime": True,
                                    "input": [
                                        0,
                                        0,
                                        0,
                                        0
                                    ],
                                    "hdop": 0.0,
                                    "ignicion": 0,
                                    "adc": [
                                        -200.0,
                                        -200.0,
                                        -200.0,
                                        -200.0
                                    ],
                                    "power": 0,
                                    "horometro": 0,
                                    "odometro": 0,
                                    "panico": 0,
                                    "bateria": 0.0,
                                    "bateriaInt": 0.0,
                                    "patente": query.patente,
                                    "tercerojo": 0,
                                    "aceleracion": 0,
                                    "frenada": 0,
                                    "giro": 0
                                }
                        ]

                    url = "https://api.waypoint.cl/inbound/inboundLD"

                    payload = json.dumps(payload)
                    headers = {
                        'Content-Type': 'application/json',
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    if response.status_code == 200:

                        code_response = json.loads(response.json())
                        if int(code_response["code"]) == 0:
                            
                            query_exist = get_data_integraciones_sinc(query.imei)

                            data_integraciones_sinc = {
                                "sinc_integ": load_data('INTEGRATION_NAME'),
                                "sinc_imei": query.imei,
                                "sinc_dt_tracker": query.fecha_tracker,
                                "sinc_dt_server": query.dt_server,
                                "sinc_params": query.params,
                                "sinc_lat": query.latitud,
                                "sinc_lng": query.longitud,
                                "sinc_speed": query.velocidad,
                                "sinc_angle": query.angle,
                                "sinc_plate": query.patente,
                                "idpoint": 0
                            }

                            if query_exist.rowcount == 0:
                                insert_integraciones_sinc(data_integraciones_sinc)
                                Logger.add_to_log("success", f"insert: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")

                            else:
                                update_integraciones_sinc(data_integraciones_sinc)
                                Logger.add_to_log("success", f"update: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")

                            Logger.add_to_log("success", f"punto enviado: {query.patente}", load_data('LOG_DIRECTORY'), "log_waypoint")
                        else:

                            error_integracion = response.json()
                            Logger.add_to_log("error", error_integracion, load_data('LOG_DIRECTORY'), "log_waypoint")
                            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")

                    else:
                        raise ValueError("Error al enviar los datos al servidor")
        
        except ValueError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_waypoint")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")
        
        except SQLAlchemyError as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_waypoint")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")

        except Exception as ex:
            Logger.add_to_log("error", str(ex), load_data('LOG_DIRECTORY'), "log_waypoint")
            Logger.add_to_log("error", traceback.format_exc(), load_data('LOG_DIRECTORY'), "log_waypoint")
