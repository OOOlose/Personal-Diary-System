# hive_connector.py
from pyhive import hive
import pandas as pd
from config import Config


class HiveConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接 Hive"""
        try:
            self.connection = hive.connect(
                host=Config.HIVE_HOST,
                port=Config.HIVE_PORT,
                username=Config.HIVE_USER,
                database=Config.HIVE_DATABASE,
                auth='NOSASL'
            )
            self.cursor = self.connection.cursor()
            print("✅ Hive 连接成功")
            return True
        except Exception as e:
            print(f"❌ Hive 连接失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, sql):
        """执行查询并返回结果"""
        try:
            self.cursor.execute(sql)
            columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
            rows = self.cursor.fetchall()
            return {'columns': columns, 'rows': rows, 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}

    def get_expense_ratio(self):
        """获取支出占比"""
        sql = """
            SELECT 
                CASE 
                    WHEN expense > 0 THEN '正常支出'
                    WHEN expense = 0 THEN '无支出'
                    ELSE '退款/异常'
                END as expense_type,
                ROUND(SUM(ABS(expense)), 2) as total_expense,
                COUNT(*) as count
            FROM dwd_diary
            WHERE expense IS NOT NULL
            GROUP BY 
                CASE 
                    WHEN expense > 0 THEN '正常支出'
                    WHEN expense = 0 THEN '无支出'
                    ELSE '退款/异常'
                END
        """
        return self.execute_query(sql)

    def get_mood_trend(self):
        """获取心情趋势"""
        sql = """
            SELECT 
                `date`,
                ROUND(AVG(mood), 2) as avg_mood
            FROM dwd_diary
            WHERE `date` IS NOT NULL
            GROUP BY `date`
            ORDER BY `date`
            LIMIT 100
        """
        return self.execute_query(sql)

    def get_reading_exercise(self):
        """获取阅读运动统计"""
        sql = """
            SELECT 
                WEEKOFYEAR(`date`) as week_num,
                ROUND(SUM(reading_time), 2) as total_reading,
                ROUND(SUM(exercise_time), 2) as total_exercise
            FROM dwd_diary
            WHERE `date` IS NOT NULL
              AND reading_time >= 0
              AND exercise_time >= 0
            GROUP BY WEEKOFYEAR(`date`)
            ORDER BY week_num
        """
        return self.execute_query(sql)

    def get_inspiration_hour(self):
        """获取灵感时段统计"""
        sql = """
            SELECT 
                HOUR(`date`) as hour,
                COUNT(*) as count
            FROM dwd_diary
            WHERE `date` IS NOT NULL
            GROUP BY HOUR(`date`)
            ORDER BY hour
        """
        return self.execute_query(sql)

    def get_summary(self):
        """获取统计摘要"""
        sql = """
            SELECT 
                COUNT(*) as total_records,
                ROUND(AVG(mood), 2) as avg_mood,
                ROUND(SUM(CASE WHEN expense>0 THEN expense ELSE 0 END), 2) as total_expense,
                ROUND(AVG(reading_time), 2) as avg_reading,
                ROUND(AVG(exercise_time), 2) as avg_exercise
            FROM dwd_diary
        """
        return self.execute_query(sql)