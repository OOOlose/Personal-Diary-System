# config.py
import os


class Config:
    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'diary-system-secret-key')

    # Hive 配置
    HIVE_HOST = '192.168.88.131'
    HIVE_PORT = 10000
    HIVE_USER = 'root'
    HIVE_DATABASE = 'diary_db'

    # MySQL 配置（用于存储用户录入数据）
    MYSQL_HOST = '192.168.88.131'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DATABASE = 'diary_db'

    # 文件上传配置
    UPLOAD_FOLDER = '/tmp/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB