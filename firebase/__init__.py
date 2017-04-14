import os
from . import fb_config
from pyrebase.pyrebase import Firebase
from oauth2client.service_account import ServiceAccountCredentials as SAC
from oauth2client.crypt import Signer

FIREBASE_JS_CONFIG = fb_config.FIREBASE_JS_CONFIG_DEV
FIREBASE_CONFIG = fb_config.FIREBASE_CONFIG_DEV

if os.environ.get('HEROKU_RT'):
    # if production env
    FIREBASE_JS_CONFIG = fb_config.FIREBASE_JS_CONFIG_PROD
    FIREBASE_CONFIG = fb_config.FIREBASE_CONFIG_PROD


class CustomFirebase(Firebase):
    scopes = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email',
    "https://www.googleapis.com/auth/cloud-platform"
    ]

    fb_key = os.environ.get('FIREBASE_PRIVATE_KEY') or ''
    signer = Signer.from_string(fb_key.replace('\\n', '\n'))

    creds = {
    'scopes': scopes,
    'signer': signer,
    'service_account_email': os.environ.get('FIREBASE_CLIENT_EMAIL'),
    'private_key_id': os.environ.get('FIREBASE_PRIVATE_KEY_ID')

    }

    def __init__(self, config):
        super(CustomFirebase, self).__init__(config)
        self.credentials = SAC(**self.creds)

firebase = CustomFirebase(FIREBASE_CONFIG)


