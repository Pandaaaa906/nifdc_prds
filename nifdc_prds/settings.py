from os import getenv

DATABASE = {
    'database': getenv('DATABASE', 'postgres'),
    'user': getenv('DB_USER', 'postgres'),
    'host': getenv('DB_HOST', 'localhost'),
    'port': int(getenv('DB_PORT', '5432')),
    'password': getenv('DB_PASSWORD', 'postgres'),
}

WEB_USER = getenv('WEB_USER')
WEB_PASS = getenv('WEB_PASS')
