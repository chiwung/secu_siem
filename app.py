import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
DB_NAME = "security_access.db"

# ==========================================
# 1단계: 데이터베이스 초기화 및 더미 데이터 적재
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 접근 로그 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_id TEXT,
            source_ip TEXT,
            login_failed_count INTEGER,
            access_duration INTEGER,
            is_anomaly INTEGER DEFAULT 0,
            anomaly_score REAL DEFAULT 0.0
        )
    ''')
    
    # 데이터가 없을 경우에만 더미 데이터(정상 패턴 + 이상 패턴) 적재
    cursor.execute("SELECT COUNT(*) FROM access_logs")
    if cursor.fetchone()[0] == 0:
        print("💡 초기 더미 로그 데이터를 생성합니다...")
        dummy_logs = []
        
        # 정상 패턴 (주로 주간 시간대, 실패 횟수 적음)
        for i in range(1, 41):
            dummy_logs.append((f"2026-06-16 {np.random.randint(9, 18)}:{np.random.randint(10, 59)}:00", f"user_{i}", f"192.168.1.{i}", np.random.randint(0, 2), np.random.randint(10, 300)))
            
        # 이상 패턴 (새벽 시간대, 대량의 실패 횟수 - Brute Force 의심)
        dummy_logs.append(("2026-06-16 02:15:00", "admin", "210.85.23.101", 15, 10))
        dummy_logs.append(("2026-06-16 03:40:00", "system_root", "103.22.45.12", 22, 5))
        # 이상 패턴 (비정상적으로 긴 세션 유지)
        dummy_logs.append(("2026-06-16 14:20:00", "guest_temp", "192.168.1.99", 0, 86400))

        cursor.executemany('''
            INSERT INTO access_logs (timestamp, user_id, source_ip, login_failed_count, access_duration)
            VALUES (?, ?, ?, ?, ?)
        ''', dummy_logs)
        conn.commit()
    conn.close()

# ==========================================
# 2단계: 데이터 전처리 및 AI 분석 (Isolation Forest)
# ==========================================
def analyze_anomalies():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM access_logs", conn)
    
    if len(df) < 5:  # 데이터가 너무 적으면 분석 불가
        conn.close()
        return

    # [컨설턴트 가이드] 피처 엔지니어링: 시간 정보에서 '시간(Hour)' 추출
    df['hour'] = df['timestamp'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour)
    
    # 학습에 사용할 특성(Feature) 선택
    features = df[['hour', 'login_failed_count', 'access_duration']]
    
    # AI 모델 선언 (Isolation Forest: 비지도학습 이상징후 탐지)
    # 오탐율(contamination)을 약 10%로 설정
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)
    
    # 예측 수행 (-1: 이상징후, 1: 정상) 및 스코어 계산
    preds = model.predict(features)
    scores = model.decision_function(features) # 낮을수록 이상함
    
    # 결과를 DB에 업데이트 (개인정보 보호를 위해 IP/ID 가공 후 화면 표시 가이드 반영)
    cursor = conn.cursor()
    for idx, row in df.iterrows():
        is_anomaly = 1 if preds[idx] == -1 else 0
        anomaly_score = round(float(-scores[idx]), 4) # 양수가 높을수록 이상하게 조정
        
        cursor.execute('''
            UPDATE access_logs 
            SET is_anomaly = ?, anomaly_score = ? 
            WHERE id = ?
        ''', (is_anomaly, anomaly_score, int(row['id'])))
    
    conn.commit()
    conn.close()

# 개인정보 비식별화 (마스킹) 헬퍼 함수
def masking_id(user_id):
    if len(user_id) <= 3: return "***"
    return user_id[:3] + "*" * (len(user_id) - 3)

def masking_ip(ip):
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.***"
    return ip

# ==========================================
# 3단계: Flask 웹 UI 및 웹 템플릿
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>AI 기반 접근 로그 모니터링 시스템</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #f5f7fa; }
        h1, h2 { color: #2c3e50; }
        .btn { background-color: #3498db; color: white; padding: 10px 15px; border: none; cursor: pointer; border-radius: 4px; font-size: 14px;}
        .btn-danger { background-color: #e74c3c; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #34495e; color: white; }
        tr.anomaly { background-color: #fce4d6; color: #c00000; font-weight: bold; }
        .badge { padding: 5px 10px; border-radius: 12px; font-size: 12px; color: white; }
        .badge-danger { background-color: #e74c3c; }
        .badge-success { background-color: #2ecc71; }
        .container { display: flex; gap: 20px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); flex: 1; }
    </style>
</head>
<body>

    <h1>🛡️ AI 기반 접근 로그 모니터링 시스템</h1>
    <p>정보보안 실무 가이드: 수집된 접근 로그를 AI(Isolation Forest)가 분석하여 평소와 다른 이상징후를 자동 식별합니다.</p>
    
    <div class="container">
        <div class="card">
            <h3>🤖 AI 모델 제어</h3>
            <p>신규 로그가 수집되었거나, 탐지 모델을 갱신하려면 분석을 실행하세요.</p>
            <a href="/run-analysis"><button class="btn">🔄 AI 이상징후 분석 실행</button></a>
        </div>
        <div class="card">
            <h3>📝 실시간 접근 로그 시뮬레이션</h3>
            <form action="/add-log" method="POST">
                <input type="text" name="user_id" placeholder="사용자 ID" required>
                <input type="text" name="source_ip" placeholder="출발지 IP" required>
                <input type="number" name="failed_count" placeholder="로그인 실패 횟수" required style="width:110px;">
                <input type="number" name="duration" placeholder="접속 유지시간(초)" required style="width:120px;">
                <button type="submit" class="btn btn-danger">⚡ 로그 주입</button>
            </form>
        </div>
    </div>

    <h2>📊 접근 로그 점검 현황 (최근 50개)</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>접근 시간</th>
                <th>사용자 ID (비식별화)</th>
                <th>출발지 IP (비식별화)</th>
                <th>로그인 실패 횟수</th>
                <th>접속 유지(초)</th>
                <th>AI 위험도 스코어</th>
                <th>탐지 상태</th>
            </tr>
        </thead>
        <tbody>
            {% for log in logs %}
            <tr class="{% if log.is_anomaly == 1 %}anomaly{% endif %}">
                <td>{{ log.id }}</td>
                <td>{{ log.timestamp }}</td>
                <td>{{ log.masked_user }}</td>
                <td>{{ log.masked_ip }}</td>
                <td>{{ log.login_failed_count }}회</td>
                <td>{{ log.access_duration }}초</td>
                <td>{{ log.anomaly_score }}</td>
                <td>
                    {% if log.is_anomaly == 1 %}
                    <span class="badge badge-danger">⚠️ 이상 접근 위협</span>
                    {% else %}
                    <span class="badge badge-success">정상</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

</body>
</html>
"""

# ==========================================
# 4단계: 라우팅 및 비즈니스 로직
# ==========================================
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # 최신 로그 50개 조회
    cursor.execute("SELECT * FROM access_logs ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    
    # 개인정보 비식별화 처리 후 전달 (컨설턴트 가이드: 1단계 규제 준수 반영)
    processed_logs = []
    for row in rows:
        log_dict = dict(row)
        log_dict['masked_user'] = masking_id(row['user_id'])
        log_dict['masked_ip'] = masking_ip(row['source_ip'])
        processed_logs.append(log_dict)
        
    return render_template_string(HTML_TEMPLATE, logs=processed_logs)

@app.route('/add-log', methods=['POST'])
def add_log():
    """새로운 로그 주입 시뮬레이터"""
    user_id = request.form['user_id']
    source_ip = request.form['source_ip']
    failed_count = request.form['failed_count']
    duration = request.form['duration']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO access_logs (timestamp, user_id, source_ip, login_failed_count, access_duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, user_id, source_ip, failed_count, duration))
    conn.commit()
    conn.close()
    
    # 로그가 새로 들어오면 자동으로 AI 분석 갱신 구동
    analyze_anomalies()
    return redirect(url_for('index'))

@app.route('/run-analysis')
def run_analysis():
    """AI 분석 수동 갱신 수동 라우트"""
    analyze_anomalies()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()          # DB 및 데이터 초기화
    analyze_anomalies() # 초기 AI 분석 수행
    app.run(debug=True, port=5000)
