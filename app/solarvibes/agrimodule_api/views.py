from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from solarvibes import db

from solarvibes.models import User, Agrimodule, Agripump, Measurement, Agrisensor
from solarvibes.models import AgrimoduleList
from flask_login import current_user
from flask_security import login_required

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#############################################################################################################################
########################                      Blueprint
#############################################################################################################################
agrimodule_api = Blueprint('api', __name__)


#############################################################################################################################
########################                      Api OBJ
#############################################################################################################################
api = Api(agrimodule_api)


#############################################################################################################################
########################                      INDEX
#############################################################################################################################
class Index(Resource):
    def get(self):
        # return dict(welcone = 'This is the Solarvibes API design for the agrimodules to interact with Solarvibes servers!')
        return {'Welcome':'This is the Solarvibes API design for the agrimodules to interact with Solarvibes servers!'}


#############################################################################################################################
########################                      0 - CHECK
#############################################################################################################################
class Check(Resource):
    def get(self, identifier):
        # initial validation for whene a request contains no identifier
        if not identifier:
            print(identifier)
            return {'message' : 'Bad request!'}, 400

        try:
            # initialization of variables to be returned
            http_status = 202
            payload = dict(belong_to_user = False,
                            being_used = False,
                            message = 'You have not been bought or registered in a farmer account yet!',
                            )

            # query to retrieve the agrimodule registry - where the flags and to which user in the account the agrimodule belongs to.
            # db exclusive for license and tranfer of ownership of agrimodule
            agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()

            # check if identifier even exist // if this agrmiodule has a license mto access the app
            # if not  the answer is return directly here, because the other validation would give an error since agrimodule_reg would a Nonetype obj and it would not ahve atrributes
            if not agrimodule_reg:
                http_status = 403
                payload.update(message = 'Contact Solarvibes: Agrimodule Support!')
                return payload, http_status

            # if a user has registered the agrimodule to his account
            if agrimodule_reg.has_user_registered:
                http_status = 206
                payload.update(message = 'Yes, you have an owner', belong_to_user = True)

            # if a user has registered, may have deleted from its configuration, and there is not point of sending data nowhere
            agrimodule = Agrimodule.query.filter_by(identifier = identifier).first()
            if agrimodule:
                http_status = 200
                payload.update(message = 'Yes, you have an owner and your are being used', being_used = True)

            # validation to sen
            return payload, http_status
        except:
            # in case of exceptions, return a internal server error 500
            return {'error':'Internal server error agrimodule API - FIRST CONTACT!'}, 500


# TODO: is not returning the data in return for post
# TODO: is complaining the the url is mispeelled
#############################################################################################################################
########################                      1 - REGISTRATION
#############################################################################################################################

##############      register      #################
register_parser = reqparse.RequestParser()
register_parser.add_argument('identifier',
    dest = 'identifier',
    required = True,
    help = 'This is the unique token for the specific agrimodule device. it comes in the form of a QR code'
)

register_parser.add_argument('mac',
    dest = 'mac',
    required = True,
    help = 'This is the mac address for agrimodule device.'
)

register_fields = {
    'identifier' : fields.String(default = 'loco'),
    'mac' : fields.String(default = 'loco1'),
}
####################################################

class Register(Resource):
    @marshal_with(register_fields)
    def post(self):
        args = register_parser.parse_args()
        print(args.mac, args.identifier)

        # try:
        ###################################
        ###################################
        # initial validation. as in first contact
        ###################################
        def agrimodule_validation(identifier):
            # initialization of variables to be returned
            http_status = 200
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
            return msg, http_status

        ###################################
        # call initial validation
        res_msg, res_http_status = agrimodule_validation(args.identifier)
        if not res_http_status == 200:
            print(res_msg)
            print(res_http_status)
            return {'message' : res_msg}, res_http_status
        ###################################
        ###################################

        ###################################
        # Begin route
        ###################################
        http_status = 202
        payload = dict(message = 'You are in the process of registering!')

        # check if the mac address is already registered in the agrimodules register in the server
        mac_registered = Agrimodule.query.filter_by(mac = args.mac).first()
        if not mac_registered:
            # generate the public id and add the mac address to the agrimodule
            http_status = 201

            agrimodule_reg = AgrimoduleList.query.filter_by(identifier = args.identifier).first_or_404()
            agrimodule_reg.has_agrimodule_registered = True

            agrimodule = Agrimodule.query.filter_by(identifier = args.identifier).first_or_404()
            agrimodule.public_id = str(uuid.uuid4())
            agrimodule.mac = str(args.mac)

            db.session.commit()
            payload.update(password = agrimodule.mac, username = agrimodule.public_id, message = 'You have been registered')
        else:
            http_status = 403
            payload['message'] = 'This agrimodule already exist - Get Agrimodule Support!'

        # validation to send
        print(payload)
        # return {'error': 'locoooooo'}, 500
        return payload, http_status
        # except Exception as e:
        #     print('Error: ' + str(e))
        #     db.session.rollback()
        #     # in case of exceptions, return a internal server error 500
        #     return {'error': str(e)}, 500
        #     # return {'error':'Internal server error agrimodule API - REGISTERING!'}, 500


#############################################################################################################################
########################                      Resource resgistration and blueprint
#############################################################################################################################
api.add_resource(Index, '/')
api.add_resource(Check, '/check/<identifier>')
api.add_resource(Register, '/register')

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

# ERRORS
# 200, OK
# 201, Created
# 202, Accepted
# 403, Forbidden
# 206, Partial Content
