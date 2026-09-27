# app.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from hive_connector import HiveConnector

app = Flask(__name__, static_folder='../', static_url_path='')
CORS(app)

# 创建 Hive 连接器
hive_connector = HiveConnector()


# ===================== 页面路由 =====================
@app.route('/')
def home():
    return send_from_directory('../', 'dashboard.html')


@app.route('/dashboard.html')
def dashboard():
    return send_from_directory('../', 'dashboard.html')


@app.route('/input.html')
def input_page():
    return send_from_directory('../', 'input.html')


@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('../data', filename)


# ===================== API 根路径 =====================
@app.route('/api/')
def api_root():
    return jsonify({
        'name': '个人数字化日记系统 API',
        'description': '提供 Hive 数据仓库的查询接口',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': [
            {'path': '/health', 'method': 'GET', 'description': '健康检查'},
            {'path': '/api/hive/expense', 'method': 'GET', 'description': '支出占比'},
            {'path': '/api/hive/mood', 'method': 'GET', 'description': '心情趋势'},
            {'path': '/api/hive/activity', 'method': 'GET', 'description': '阅读运动'},
            {'path': '/api/hive/inspiration', 'method': 'GET', 'description': '灵感时段'},
            {'path': '/api/hive/summary', 'method': 'GET', 'description': '统计摘要'}
        ]
    })


# ===================== 健康检查 =====================
@app.route('/health')
def health():
    try:
        if not hive_connector.connect():
            return jsonify({'status': 'error', 'hive': '连接失败'}), 500
        hive_connector.disconnect()
        return jsonify({'status': 'ok', 'hive': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'hive': str(e)}), 500


# ===================== Hive 数据 API =====================
@app.route('/api/hive/expense')
def get_expense():
    try:
        if not hive_connector.connect():
            return jsonify({'error': 'Hive 连接失败'}), 500
        result = hive_connector.get_expense_ratio()
        hive_connector.disconnect()

        if result['success']:
            data = [{'expense_type': row[0], 'total_expense': row[1]} for row in result['rows']]
            return jsonify(data)
        return jsonify({'error': result.get('error')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hive/mood')
def get_mood():
    try:
        if not hive_connector.connect():
            return jsonify({'error': 'Hive 连接失败'}), 500
        result = hive_connector.get_mood_trend()
        hive_connector.disconnect()

        if result['success']:
            data = [{'date': row[0], 'avg_mood': row[1]} for row in result['rows']]
            return jsonify(data)
        return jsonify({'error': result.get('error')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hive/activity')
def get_activity():
    try:
        if not hive_connector.connect():
            return jsonify({'error': 'Hive 连接失败'}), 500
        result = hive_connector.get_reading_exercise()
        hive_connector.disconnect()

        if result['success']:
            data = [{'week_num': row[0], 'total_reading': row[1], 'total_exercise': row[2]} for row in result['rows']]
            return jsonify(data)
        return jsonify({'error': result.get('error')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hive/inspiration')
def get_inspiration():
    try:
        if not hive_connector.connect():
            return jsonify({'error': 'Hive 连接失败'}), 500
        result = hive_connector.get_inspiration_hour()
        hive_connector.disconnect()

        if result['success']:
            data = [{'hour': row[0], 'count': row[1]} for row in result['rows']]
            return jsonify(data)
        return jsonify({'error': result.get('error')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hive/summary')
def get_summary():
    try:
        if not hive_connector.connect():
            return jsonify({'error': 'Hive 连接失败'}), 500
        result = hive_connector.get_summary()
        hive_connector.disconnect()

        if result['success'] and result['rows']:
            row = result['rows'][0]
            return jsonify({
                'total_records': row[0],
                'avg_mood': row[1],
                'total_expense': row[2],
                'avg_reading': row[3],
                'avg_exercise': row[4]
            })
        return jsonify({})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("个人数字化日记系统 - 后端服务")
    print("=" * 60)
    print("服务地址: http://localhost:5000")
    print("API 文档: http://localhost:5000/api/")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)