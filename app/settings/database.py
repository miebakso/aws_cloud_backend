from app.settings.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database():
    settings = get_settings()
    host = settings.DB_HOST
    username = settings.DB_USERNAME
    password = settings.DB_PASSWORD
    port = settings.DB_PORT
    dbname = settings.DB_NAME
    access_key = settings.aws_access_key_id
    secret_key = settings.aws_secret_access_key
    session_token = settings.aws_session_token
    bucket_name = settings.AWS_BUCKET_NAME
    URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
    # print(URL)
    engine = create_engine(URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()
    
    def get_engine(self):
        return self.engine


# import pymysql
# connect = pymysql.connect(settings.DB_HOST, settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_PORT)
# cursor = connect.cursor()
# curosr.exec()
# cursor.close()
