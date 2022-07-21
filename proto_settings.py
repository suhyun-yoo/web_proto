DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'protodb',
        'USER': 'protouser',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
           'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           'charset': 'utf8mb4',
           'use_unicode': True,
       },
    }
}