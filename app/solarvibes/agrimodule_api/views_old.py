

# @agrimodule_api.route('/', methods = ['GET'])
# # @login_required
# def index():
#     return jsonify({'welcome':'check the API to play with Solarvibes!'})


# TODO: roles and authentication for current user must be done in order to retreive users agrimodules
@agrimodule_api.route('/agrimodules', methods = ['GET'])
# @login_required
def get_agrimodules():

    agrimodules = User.query.filter_by(id = 1).first().agrimodules.all()

    # create an empty list
    payload = list()
    for agrimodule in agrimodules:
        # add a dictionary per agrimodule into the list
        payload.append(dict( id = agrimodule.id,
                        system_name = agrimodule.name,
                        user_id = agrimodule.user_id,
                        field_id = agrimodule.field_id,
                        ))

    # make a dictionary as main key 'agrimodules' with a the list of dictionaries to be jsonify
    payload = dict(agrimodules = payload)
    return jsonify(payload)


@agrimodule_api.route('/agrimodule', methods = ['GET'])
@agrimodule_api.route('/agrimodule/<agrimodule_id>', methods = ['GET'])
@login_required
def get_agrimodule(agrimodule_id = None):

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify({'message':'agrimodule do not exist!'})

    agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).one()
    return jsonify(agrimodule)



#############################################################################################################################
#############################################################################################################################
########################                      SET MEASUREMENT
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/set-measurement', methods = ['POST'])
# @login_required
def set_measurement(agrimodule_id = None):

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))


    data = request.get_json()
    print(data)
    print(request.data)
    print(type(data['agrimodule_id']))
    print(data['timestamp'])
    print(type(data['timestamp']))
    print(type(data['soil_ph']))
    print(type(data['soil_nutrient']))
    print(type(data['soil_temp']))
    print(type(data['soil_humi']))
    print(type(data['air_temp']))
    print(type(data['air_humi']))
    print(type(data['air_pres']))
    print(type(data['solar_radiation']))
    print(type(data['batt_status']))
    print(type(data['lat']))
    print(type(data['lon']))
    if request.method == 'POST':
        try:
            payload = request.get_json()
            measurement = Measurement(  agrimodule_id = int(payload['agrimodule_id']),
                                        timestamp = datetime(payload['timestamp']),
                                        soil_ph = float(payload['soil_ph']),
                                        soil_nutrient = float(payload['soil_nutrient']),
                                        soil_temp = float(payload['soil_temp']),
                                        soil_humi = float(payload['soil_humi']),
                                        air_temp = float(payload['air_temp']),
                                        air_humi = float(payload['air_humi']),
                                        air_pres = float(payload['air_pres']),
                                        solar_radiation = float(payload['solar_radiation']),
                                        batt_status = int(payload['batt_status']),
                                        lat = float(payload['lat']),
                                        lon = float(payload['lon']),
                                        )
            # set agrimodule with lates batt_status, lat and lon
            agrimodule.batt_status = int(payload['batt_status'])
            agrimodule.lat = float(payload['lat'])
            agrimodule.lon = float(payload['lon'])
            # add object to db and save
            db.session.add(measurement)
            db.session.commit()
            return jsonify({'message':'measurement created!'})
        except:
            db.session.rollback()
            return jsonify({'error':'measurement not created!'})

    return jsonify(dict(message = 'FANTASO ERROR'))

#############################################################################################################################
#############################################################################################################################
########################                      GET MEASUREMENT
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurement', methods = ['GET'])
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurement/<measurement_id>', methods = ['GET'])
# @login_required
def get_measurement(agrimodule_id = None, measurement_id = None):



    if not agrimodule_id or not measurement_id:
        print(agrimodule_id, measurement_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))

    measurement = agrimodule.measurements.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify(dict(message = 'measurement do not belong to agrimodule!'))

    if request.method == 'GET':
        try:
            # create a dict with data from db
            payload = dict( measurement_id = measurement.id,
                            agrimodule_id = measurement.agrimodule_id,
                            timestamp = measurement.timestamp,
                            soil_ph = measurement.soil_ph,
                            soil_nutrient = measurement.soil_nutrient,
                            soil_temp = measurement.soil_temp,
                            soil_humi = measurement.soil_humi,
                            air_temp = measurement.air_temp,
                            air_humi = measurement.air_humi,
                            air_pres = measurement.air_pres,
                            solar_radiation = measurement.solar_radiation,
                            batt_status = measurement.batt_status,
                            lat = measurement.lat,
                            lon = measurement.lon,
                            )

            # make a dictionary as main key 'measurement' with a the list of dictionaries to be jsonify
            payload = dict(measurement = payload)
            return jsonify(payload)
        except:
            return jsonify({'error':'measurement corrupted!'})



#############################################################################################################################
#############################################################################################################################
########################                      GET MEASUREMENTS
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurements', methods = ['GET'])
@login_required
def get_measurements(agrimodule_id = None):

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))

    measurement = agrimodule.measurements.first()
    if not measurement:
        return jsonify(dict(message = 'agrimodule have not recoreded a measurement!'))

    measurements = agrimodule.measurements.all()

    if request.method == 'GET':
        try:
            # create an empty list
            payload = list()
            for measurement in measurements:
                # add a dictionary per agrimodule into the list
                payload.append(dict(    measurement_id = measurement.id,
                                        agrimodule_id = measurement.agrimodule_id,
                                        timestamp = measurement.timestamp,
                                        soil_ph = measurement.soil_ph,
                                        soil_nutrient = measurement.soil_nutrient,
                                        soil_temp = measurement.soil_temp,
                                        soil_humi = measurement.soil_humi,
                                        air_temp = measurement.air_temp,
                                        air_humi = measurement.air_humi,
                                        air_pres = measurement.air_pres,
                                        solar_radiation = measurement.solar_radiation,
                                        batt_status = measurement.batt_status,
                                        lat = measurement.lat,
                                        lon = measurement.lon,
                                        ))

            # make a dictionary as main key 'measurements' with a the list of dictionaries to be jsonify
            payload = dict(measurements = payload)
            return jsonify(payload)
        except:
            return jsonify({'error':'all measurements corrupted!'})





#############################################################################################################################
#############################################################################################################################
########################                      1 - UN-REGISTRATION
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/unregister', methods = ['GET'])
@agrimodule_api.route('/unregister/<identifier>', methods = ['GET'])
@agrimodule_api.route('/unregister/<identifier>/<mac>', methods = ['GET'])
# @login_required
def unregister(identifier = None, mac = None):

    # initial validation for whene a request contains no identifier
    if not identifier or not mac:
        print(identifier, mac)
        return jsonify(dict(message = 'not allowed!')), 400

    # return jsonify(dict(message = 'You have not yet been bought or registered in a farmer account!',)), 202
    if request.method == 'GET':
        try:
            ###################################
            ###################################
            # initial validation. as in first contact
            ###################################
            def agrimodule_validation(identifier = None):
                # initialization of variables to be returned
                http_status = None
                msg = 'You have not been bought or registered in a farmer account yet!'
                # query to retrieve the agrimodule registry - where the flags and to which user in the account the agrimodule belongs to.
                # db exclusive for license and tranfer of ownership of agrimodule
                agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
                # check if identifier even exist // if this agrmiodule has a license mto access the app
                # if not  the answer is return directly here, because the other validation would give an error since agrimodule_reg would a Nonetype obj and it would not ahve atrributes
                if not agrimodule_reg:
                    http_status = 403
                    msg = 'Contact Solarvibes: Agrimodule Support!'
                    return dict(msg = msg, http_status = http_status)
                # if a user has registered the agrimodule to his account
                if agrimodule_reg.has_user_registered:
                    http_status = 206
                    msg = 'Yes, you have an owner'
                # if a user has registered, may have deleted from its configuration, and there is not point of sending data nowhere
                agrimodule = Agrimodule.query.filter_by(identifier = identifier).first()
                if agrimodule:
                    http_status = 200
                    msg = 'Yes, you have an owner and your are being used'
                # validation to sen
                return dict(msg = msg, http_status = http_status)

            ###################################
            # call initial validation
            response = agrimodule_validation(identifier)
            if not response['http_status'] == 200:
                return jsonify(dict(message = response['msg'])), response['http_status']
            ###################################
            ###################################


            ###################################
            # Begin route
            ###################################
            http_status = 202
            payload = dict(message = 'You are in the process of registering!')

            # check if the mac address is already registered in the agrimodules register in the server
            mac_registered = Agrimodule.query.filter_by(mac = mac).first()
            if not mac_registered:
                # generate the public id and add the mac address to the agrimodule
                http_status = 201

                agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
                agrimodule_reg.has_agrimodule_registered = True

                agrimodule = Agrimodule.query.filter_by(identifier = identifier).first()
                agrimodule.public_id = str(uuid.uuid4())
                agrimodule.mac = str(mac)

                db.session.commit()
                payload.update(password = agrimodule.mac, username = agrimodule.public_id, message = 'You have been registered')
            else:
                http_status = 403
                payload.update(message = 'This agrimodule already exist: Get Agrimodule Support!')

            # validation to send
            return jsonify(payload), http_status
        except Exception as e:
            print('Error: ' + str(e))
            db.session.rollback()
            # in case of exceptions, return a internal server error 500
            return jsonify({'error': str(e)}), 500

#### flask-restless basic configuration.
# from flask_restless import APIManager
# manager = APIManager(application, flask_sqlalchemy_db = db)
# manager.create_api(Agrimodule)
# manager.create_api(Agrisensor, methods=['GET'])
# manager.create_api(Agripump, methods=['GET'])
# manager.create_api(Measurement, methods=['GET','POST'])

# # print(ag_measurement.timestamp)
# # print(ag_measurement.soil_ph)
# # print(ag_measurement.soil_nutrient)
# # print(ag_measurement.soil_temp)
# # print(ag_measurement.soil_humi)
# # print(ag_measurement.air_temp)
# # print(ag_measurement.air_humi)
# # print(ag_measurement.air_pres)
# # print(ag_measurement.solar_radiation)
# # print(ag_measurement.batt_status)
# # print(ag_measurement.lat)
# # print(ag_measurement.lon)
