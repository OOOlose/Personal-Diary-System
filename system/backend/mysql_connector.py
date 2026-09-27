# mysql_connector.py
import pymysql
from config import Config


class MySQLConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接 MySQL"""
        try:
            self.connection = pymysql.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("✅ MySQL 连接成功")
            return True
        except Exception as e:
            print(f"❌ MySQL 连接失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def init_table(self):
        """初始化用户日记表"""
        sql = """
            CREATE TABLE IF NOT EXISTS user_diary (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                mood INT NOT NULL,
                expense DECIMAL(10,2) DEFAULT 0,
                reading_time INT DEFAULT 0,
                exercise_time INT DEFAULT 0,
                inspire TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(sql)
        self.connection.commit()
        print("✅ 用户日记表初始化完成")

    def insert_diary(self, data):
        """插入日记记录"""
        sql = """
            INSERT INTO user_diary (date, mood, expense, reading_time, exercise_time, inspire)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            data['date'], data['mood'], data['expense'],
            data['reading_time'], data['exercise_time'], data['inspire']
        ))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_diaries(self, limit=50):
        """获取所有日记记录"""
        sql = "SELECT * FROM user_diary ORDER BY date DESC LIMIT %s"
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()

    def delete_diary(self, diary_id):
        """删除日记记录"""
        sql = "DELETE FROM user_diary WHERE id = %s"
        self.cursor.execute(sql, (diary_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def clear_all(self):
        """清空所有记录"""
        sql = "TRUNCATE TABLE user_diary"
        self.cursor.execute(sql)
        self.connection.commit()