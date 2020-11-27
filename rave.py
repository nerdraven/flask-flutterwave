from flask import current_app, _app_ctx_stack, Flask
from rave_python import Rave, RaveExceptions, Misc
from .errors import ConfigError

class RavePay:
    def __init__(self, app=None):
        self.app = app
        self.flutter_wave_ref = dict()
        if app is not None:
            self.init_app(app)
    
    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'rave'):
                ctx.rave = self.connect()
        return ctx.rave

    def init_app(self, app):
        if app.config['RAVE_SECRET_KEY'] == '' \
                or app.config['RAVE_PUBLIC_KEY'] == '':
            raise ConfigError(
                    message="RAVE_SECRET_KEY or RAVE_PUBLIC_KEY not set")
        self.app = app

    def connect(self):
        PUB_KEY = self.app.config['RAVE_PUBLIC_KEY']
        SEC_KEY = self.app.config['RAVE_SECRET_KEY']
        # ENC_KEY = environ.get('RAVE_ENCRYPTION_KEY')
        rave = Rave(PUB_KEY, SEC_KEY)
        return rave

    def charge(self, person: dict, amount, pin):
        ''' Get all payment attributes ready else break '''
        self.verify_person(person)

        try:
            res = self.connection.Card.charge(person)
            self.flutter_wave_ref = res['flwRef']
            Misc.updatePayload(res["suggestedAuth"], person, pin=pin)
            res = self.connection.Card.charge(person)
        except RaveExceptions.CardChargeError as e:
            print(e.err["errMsg"])
            print(e.err["flwRef"])
        except RaveExceptions.TransactionValidationError as e:
            print(e.err)
            print(e.err["flwRef"])

        # Save to temporary data structure
        self.flutter_wave_ref[person['firstname']] = res['flwRef']
        return True

    def otp_validate(self, firstname, pin):
        ''' Get card's PIN '''
        flwRef = self.flutter_wave_ref.pop(firstname)
        try:
            self.connection.Card.validate(flwRef, '12345')
        except RaveExceptions.TransactionVerificationError as e:
            print('TransactionVerificationError')
            print(e.err["errMsg"])
            print(e.err["txRef"])
        return True

    def verify_status(self, res):
        res = self.connection.Card.verify(res["txRef"])
        return res["transactionComplete"]

    def verify_person(self, data: dict):
        required_fields  = [
            'cardno',
            'cvv',
            'expirymonth',
            'expiryyear',
            'email',
            'phonenumber',
            'firstname',
            'lastname',
        ]

        keys = data.keys()
        for attr in required_fields:
            if attr not in keys:
                raise Exception(f'{attr} not available')
        return data