SITE_ID = 6

import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql', 
        'NAME': 'voronoi',
        'USER': 'root',
        'PASSWORD': 'size',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': "django.contrib.gis.db.backends.postgis", 
        'NAME': 'voronoi',
        'USER': 'sathish',
        'PASSWORD': 'size',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    }
}
