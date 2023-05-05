import secrets

DB_USERNAME = <db username here>
DB_PASSWORD = <db pass here>
DB_HOST = <host here>
DB_PORT = <port here>
DB_NAME = <db name here>
SALT = secrets.token_hex(<whatever number you'd like>)
SECRET = secrets.token_hex(<whatever number you'd like>)