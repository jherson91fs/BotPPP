import boto3
from config import Config

def subir_archivo_s3(archivo):
    s3 = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_KEY
    )
    
    s3.upload_file(archivo, Config.AWS_S3_BUCKET, archivo)
    return f"Archivo {archivo} subido correctamente a S3."
