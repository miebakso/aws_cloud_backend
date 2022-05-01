from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # stockforum.ca1viqidbj5j.us-east-1.rds.amazonaws.com
    DB_HOST: str = "stockforum.ca1viqidbj5j.us-east-1.rds.amazonaws.com"
    DB_PORT: str = "3306"
    DB_USERNAME: str = "admin" 
    DB_PASSWORD: str = "abcd1234"
    DB_NAME: str = "stockforum"
    aws_access_key_id='ASIAVY4INUFHFH6KHGXV'
    aws_secret_access_key='9SswgP/jeDGpUx9biQNzBOTTXqRZFx7pMvxTG7zL'
    aws_session_token='FwoGZXIvYXdzEG0aDDdtZFHD0PiYyT6v/SLNAXsh2RUwDTvrGhZfdn6/rrdLOfazCsrMydMMy3eUGCxhl/61GbW+gU9XPgukOjC9N7W2aezVGDDDAUsXE8t69PW/MPKBG13oNapR/lKI0bskpboVoNJSXU8+tN/bfPiNqf4g7QSfUC1FpN5qt9xXoW5twTAxf8dgItGUj9nFCPwfqG/OIT7p92Tk9nQ5CPdiHvdGuBnCMKPD9RjtNqY/fIu5YJG61XRxvIer+m4KMFuxscrSxF/bE2KzZKf7oJ2u/Iuq0n+82pSVzk1GhuMop/m3kwYyLUoLPsMuXuKDv8OGcQXAMz5kpc4QPGn5BOx6lqon9pJyQ5Zau1JAOqYLjZ6hDQ=='
    AWS_BUCKET_NAME = "miebakso"
    
@lru_cache()
def get_settings():
    return Settings()

