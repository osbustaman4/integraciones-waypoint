
from decouple import config as load_data
from sqlalchemy import text
from lib.Stech import Stech
from lib.Connection import Connection


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

        query_string = f"""
                SELECT
                    UNIX_TIMESTAMP(DATE_SUB(obj.dt_tracker, INTERVAL {time_zone})) AS fecha,
                    obj.lat AS latitud,
                    obj.lng AS longitud,
                    obj.altitude AS altitud,
                    obj.angle AS cog,
                    obj.speed AS velocidad,
                    obj.satelites AS nsat,
                    obj.plate_number AS patente,
                    obj.imei,
                    obj.dt_server,
                    DATE_SUB(obj.dt_tracker, INTERVAL -4 HOUR) AS fecha_tracker,
                    obj.angle,
                    obj.params

                FROM
                    gs_objects obj
                    JOIN gs_user_objects u_obj ON u_obj.imei = obj.imei
                    JOIN gs_users us ON us.id = u_obj.user_id 
                WHERE
                    us.id = {id_user};
            """

        # Ejecuta la consulta
        query_results = session.execute(text(query_string)).fetchall()
        return query_results
    
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