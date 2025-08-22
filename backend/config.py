import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    UPLOAD_FOLDER = "data/raw"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    
    # MySQL Database Configuration
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Pep20233"  #  password
    MYSQL_DATABASE = "football_coach"