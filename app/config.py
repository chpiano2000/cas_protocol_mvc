from decouple import config

BASE_URL = config('BASE_URL')
STAGING_LOGIN_URL = config('STAGING_LOGIN_URL')
STAGING_LOGOUT_URL = config('STAGING_LOGOUT_URL')
STAGING_REGISTER_URL = config('STAGING_REGISTER_URL')
STAGING_VALIDATE_URL = config('STAGING_VALIDATE_URL')
BASIC_AUTH_USERNAME = config('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = config('BASIC_AUTH_PASSWORD')