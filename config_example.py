import secrets

DB_USERNAME = 'name' # this is the name of you MySQL server, a lot of the time this is root
DB_PASSWORD = 'password' # This is the password for your
DB_HOST = 'hostname' # this is the host of your SQL server, normally localhost
DB_PORT = 1111 # this is the port, which is normally 3306
DB_NAME = 'dbname' # set this to the name of the db that was filled using the provided schema
SALT = secrets.token_hex(1) # 32 is the suggested
SECRET = secrets.token_hex(1) # 32 is the suggested

# Fill out with appropriate information