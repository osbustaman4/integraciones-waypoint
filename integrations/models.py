
from decouple import config as load_data
from sqlalchemy import text
from lib.Stech import Stech
from lib.Connection import Connection
from datetime import datetime, timezone, timedelta


def get_data_integraciones_sinc(imei):
    session = Connection.get_session(load_data('ENVIRONMENTS'))
    query_question_exist = """
                            SELECT
                                * 
                            FROM
                                integraciones_sinc 
                            WHERE
                                sinc_imei = :sinc_imei;
                        """
    
    query_exist = session.execute(text(query_question_exist), {
        "sinc_imei": imei
    })
    return query_exist
    


def response_gs_objects(time_zone, id_user):
    try:
        session = Connection.get_session(load_data('ENVIRONMENTS'))
        lst_objects = []

        query_string = f"""
                SELECT
                    obj.lat AS latitude,
                    obj.lng AS longitude,
                    obj.altitude AS altitude,
                    obj.plate_number AS vehicleCode,
                    obj.odometer AS odometer,
                    Null AS driverCode,
                    UNIX_TIMESTAMP(DATE_SUB(obj.dt_tracker, INTERVAL {time_zone})) AS start,
                    obj.speed,
                    CONCAT('";FYS;"') AS tags
                FROM
                    gs_objects obj
                    JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
                    JOIN gs_users us ON us.id = u_obj.user_id 
                WHERE
                    us.id = {id_user};
            """

        # Ejecuta la consulta
        query_results = session.execute(text(query_string)).fetchall()
        lst_objects = [
            {
                "latitude": result.latitude,
                "longitude": result.longitude,
                "altitude": result.altitude,
                "vehicleCode": str(result.vehicleCode),
                "odometer": result.odometer,
                "driverCode": result.driverCode,
                "start": datetime.fromtimestamp(result.start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "speed": result.speed,
                "tags": result.tags
            }
            for result in query_results
        ]
        return lst_objects
    
    except Exception as e:
        return str(e)


def time_zone():
    try:

        session = Connection.get_session(load_data('ENVIRONMENTS'))
        result_time_zone = session.execute(text("""SELECT timezone FROM gs_users WHERE id = 1;"""))

        response_data_timezone = [
            {
                "timezone": result.timezone,
            }
            for result in result_time_zone
        ]

        data_timezone = response_data_timezone[0]["timezone"]
        if "hour" in data_timezone.lower():
            data_timezone = data_timezone.replace("hour", "HOUR")

        return data_timezone
    
    except Exception as e:
        return str(e)


def insert_integraciones_sinc(data):
    try:
        session = Connection.get_session(load_data('ENVIRONMENTS'))

        query_insert = """
            INSERT INTO integraciones_sinc(
                sinc_integ
                ,sinc_imei
                ,sinc_dt_tracker
                ,sinc_dt_server
                ,sinc_params
                ,sinc_lat
                ,sinc_lng
                ,sinc_speed
                ,sinc_angle
                ,sinc_plate
                ,idpoint
            ) VALUES (
                :sinc_integ
                ,:sinc_imei
                ,:sinc_dt_tracker
                ,:sinc_dt_server
                ,:sinc_params
                ,:sinc_lat
                ,:sinc_lng
                ,:sinc_speed
                ,:sinc_angle
                ,:sinc_plate
                ,:idpoint
            ) ON DUPLICATE KEY UPDATE
                sinc_integ = VALUES(sinc_integ),
                sinc_imei = VALUES(sinc_imei),
                sinc_dt_tracker = VALUES(sinc_dt_tracker),
                sinc_dt_server = VALUES(sinc_dt_server),
                sinc_params = VALUES(sinc_params),
                sinc_lat = VALUES(sinc_lat),
                sinc_lng = VALUES(sinc_lng),
                sinc_speed = VALUES(sinc_speed),
                sinc_angle = VALUES(sinc_angle),
                sinc_plate = VALUES(sinc_plate),
                idpoint = VALUES(idpoint)
        """

        session.execute(text(query_insert), data)
        session.commit()

    except Exception as e:
        return str(e)


def update_integraciones_sinc(data):
    try:
        session = Connection.get_session(load_data('ENVIRONMENTS'))

        query_update = """
            UPDATE integraciones_sinc
            SET
                sinc_integ = :sinc_integ,
                sinc_imei = :sinc_imei,
                sinc_dt_tracker = :sinc_dt_tracker,
                sinc_dt_server = :sinc_dt_server,
                sinc_params = :sinc_params,
                sinc_lat = :sinc_lat,
                sinc_lng = :sinc_lng,
                sinc_speed = :sinc_speed,
                sinc_angle = :sinc_angle,
                sinc_plate = :sinc_plate,
                idpoint = :idpoint
            WHERE
                sinc_imei = :sinc_imei;
        """

        session.execute(text(query_update), data)
        session.commit()

    except Exception as e:
        return str(e)