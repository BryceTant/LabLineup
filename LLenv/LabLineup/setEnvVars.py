import os

def set(env):

    #DJANGO
    os.environ["LL_DJANGO_SECRET"] = 'a5ddfa33-1b93-4a5a-8532-afe1dafe0b3b'

    #Database
    os.environ["LL_DB_NAME"] = 'lldb'
    os.environ["LL_DB_USER"] = 'testDBUser'
    os.environ["LL_DB_PASSWORD"] = 'z5b3P9wwr9F6'
    os.environ["LL_DB_HOST"] = '35.231.63.117'
    os.environ["LL_DB_PORT"] = '3306'

    #Base URL
    if env == "dev":
        os.environ["LL_BASEURL"] = 'http://127.0.0.1:8000'
    else:
        os.environ["LL_BASEURL"] = 'https://www.LabLineup.com'

    #SendEmail / MailGun
    os.environ["LL_MAILGUN_API"] = 'https://api.mailgun.net/v3/notify.lablineup.com/messages'
    os.environ["LL_MAILGUN_API_KEY"] ='8417d7db91e6ff4430906312affaf067-816b23ef-53a937ca'
    os.environ["LL_MAILGUN_FROM"] = 'LabLineup <no-reply@lablineup.com>'

    #Payment / Square
    if env == "dev":
        os.environ["LL_SQUARE_ACCESS_TOKEN"] = 'EAAAEKhuO_dB5OIb_klu9b6LC4Z8kyyGVK6CF6oOXHFwYFe5vQHDcMWEM4DidtaB'
        os.environ["LL_SQUARE_ENV"] = 'sandbox'
        os.environ["LL_SQUARE_LOCATION"] = 'CJ5PA0KHCQEA0'
    else:
        os.environ["LL_SQUARE_ACCESS_TOKEN"] = 'EAAAEKYGlhNeE5bozB2XB58MnNtQ34R5ctaRFhcozKCNSepkXOfhkUDy9HIipiE-'
        os.environ["LL_SQUARE_ENV"] = 'production'
        os.environ["LL_SQUARE_LOCATION"] = '53F4A4TW4EXN5'
