########################################################################
# Author: Juan Angel Carrera Soto
# Last modified: 16/09/2024
# Description: Blueprint for log management.
# Functions: activity_logger
# Routes: /activity_logger
########################################################################
import os
import requests
from datetime import datetime as dt
from flask import Blueprint, request, jsonify, abort

# Blueprint
manage_logger = Blueprint('manage_logger', __name__)

# Messages
messages = {
    '400': 'Bad request',
    '403': 'Access to the requested service is forbidden',
    '500': 'Server failed to process request'
}

# Constants
LOG_ROUTE = '/flask/logs/activity/'


# Alerts reprocessing
@manage_logger.route('/activity_logger/<function>', methods=['POST'])
def activity_logger(function=None):
    """
    Log information of a request to the database.
    """
    # Get Arguments
    try:

        ignore_endpoints = [
            'refresh_token',
            'get_user_info',
            'get_usuario_notificaciones'
        ]

        # Continue if useless info
        if str(function) in ignore_endpoints:
            return jsonify({'result': 200})

        # Continue if no user info
        if 'Authorization' not in request.headers.keys():
            return jsonify({'result': 200})

        # Request necessary info
        auth = request.headers['Authorization']
        auth = str(auth).replace('Bearer ', '')
        page = request.headers['Referer']
        ip_addr = request.headers['Cf-Connecting-Ip']
        ip_country = request.headers['Cf-Ipcountry']

        # # Get user info
        # db_request = requests.post(
        #     'http://postgrest:3000/rpc/get_user_info',
        #     headers={
        #         "Authorization": 'Bearer ' + auth,
        #         'Content-Disposition': 'form-data'
        #     },
        #     data={"auth_token": auth}
        # )
        # code = db_request.status_code
        # db_request.close()
        #
        # if code != 200:
        #     abort(403, description=messages['403'])
        #
        # # Extract user info
        # username = db_request.json()['username']
        # rol = db_request.json()['rol']
        username = 'TEST-NAME'
        rol = 'TEST-ROL'

        # Get now
        moment = dt.now().strftime('%d/%m/%Y %H:%M:%S')
        year = dt.now().strftime('%Y')
        month = dt.now().strftime('%m')

        if not os.path.exists(LOG_ROUTE + '{}/{}'.format(year, month)):
            os.makedirs(LOG_ROUTE + '{}/{}'.format(year, month))

        log_file = LOG_ROUTE + '{}/{}/'.format(year, month) + username + '.log'

        with open(log_file, 'a') as f:

            parameters = 'PARAMS: '
            for k in request.json.keys():
                if 'token' not in k:
                    parameters = parameters + k + ': {} ; '.format(
                        request.json[k])

            if parameters == 'PARAMS: ':
                parameters = ''
            else:
                parameters = ' ' * (59 - len(function)) + parameters

            # Log info
            f.write(
                '[{} {} {}] USER: {} ({}) VIEW: {} ACTION: /{} {}\n'.format(
                    moment, ip_addr, ip_country, username,
                    rol, page, function, parameters
                )
            )

    except Exception:
        abort(400, description=messages['400'])

    return jsonify({'result': 200})
