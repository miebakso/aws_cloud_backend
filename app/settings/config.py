from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # stockforum.ca1viqidbj5j.us-east-1.rds.amazonaws.com
    DB_HOST: str = "stockforum.ca1viqidbj5j.us-east-1.rds.amazonaws.com"
    DB_PORT: str = "3306"
    DB_USERNAME: str = "admin" 
    DB_PASSWORD: str = "abcd1234"
    DB_NAME: str = "stockforum"
    aws_access_key_id='ASIAVY4INUFHL6GPHP5D'
    aws_secret_access_key='Y1Hk8Pv1fIlmaI6Pl/ObZE5csOTL4rmKUlQve5ff'
    aws_session_token='FwoGZXIvYXdzEM3//////////wEaDJeLEM7QcTHwZ+b2eiLNAdGLteMqWsNn92U/5ijpQ4PtvgJqOZ8z33kvlocI301pvgN6wWHkwKsVdRvO7oxSmqX8h4KpBK83JV73WttjBlmN43TjSKheiv2mC1+oC9EL4fCuOeM68s3dCK+j1OCSqDb162OFT2t8FM/ACR9Joytklrnmr8QiSF/2a5iOF4CXSxbxHKp6QjURieB2nUtGceiis+qJsMBOg8pr54bsbiEi9Byz2jNhRZL1Az9wNRsGXAOlmLyWH/gw0y7CIK6UDXk4M500FwBjC7m/81Move2UkwYyLZfCAfrkwMueGJmF6jYel1ZZcBaVg3ivr3LI6WWCsBw4UOABQw2Jm67emETokw=='
    AWS_BUCKET_NAME = "miebakso"
    
@lru_cache()
def get_settings():
    return Settings()

