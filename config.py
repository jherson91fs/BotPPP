import os

class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.getenv("MYSQL_DB", "ppp")

    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

    SAVE_LOCAL = os.getenv("SAVE_LOCAL", "True") == "True"  # True en local, False en AWS
