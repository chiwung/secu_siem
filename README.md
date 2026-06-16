# secu_siem
정보보안 로그 점검 및 모니터링 시스템에 AI(기머러닝/DL 기반 이상징후 탐지)를 도입하는 **6개월(24주) 프로젝트 일정 계획**입니다.
현업 보안 솔루션(SIEM, SOAR) 연동과 AI 모델의 오탐(False Positive)을 줄이는 데 초점을 맞추어 **기획, 데이터 준비, 모델 개발, 시스템 연동, 안정화**의 5단계로 구성했습니다.
## 📅 AI 기반 보안 로그 모니터링 프로젝트 6개월 마일스톤
```
[M1: 기획 및 인프라] -> [M2-3: 데이터 수집/가공] -> [M4: AI 모델 개발/검증] -> [M5: 시스템 연동/테스트] -> [M6: 운영 이관/안정화]

```
### 🎯 1개월 차 (1~4주): 요구사항 정의 및 인프라 구축
 * **1~2주차: 프로젝트 범위 및 목표 정의**
   * 대상 로그 선정 (FW, IDS/IPS, WAF, Windows/Linux 서버, 인증 로그 등)
   * AI 적용 유스케이스 정의 (예: 대량의 오탐 필터링, 미탐 탐지, 사용자 행동 분석(UBA))
   * 보안 및 개인정보 보호 규정(개인정보보호법, 망분리 규정 등) 검토
 * **3~4주차: 인프라 및 개발 환경 구성**
   * AI 모델 학습 및 추론을 위한 서버/GPU 인프라 확보
   * Docker, DuckDB 또는 로컬 데이터 마트 환경 등 로그 수집·적재를 위한 아키텍처 설계
   * 협업 툴 및 버전 관리(Git) 환경 세팅
### 📊 2~~3개월 차 (5~~12주): 데이터 파이프라인 구축 및 전처리 (가장 중요)
 * **5~6주차: 로그 데이터 수집 및 표준화**
   * 이 기종 장비의 로그를 단일 저장소로 수집 (Syslog, Agent 방식 등)
   * 로그 포맷 정규화 (정규표현식 파싱 및 Logstash/Fluentd 등 활용)
 * **7~10주차: 데이터 정제 및 피처 엔지니어링 (Feature Engineering)**
   * **개인정보 비식별화 처리 (주민번호, IP, 계정명 등 마스킹/암호화)**
   * 학습을 위한 피처 추출 (예: IP별 접속 빈도, 시간대별 트래픽 량, 실패 횟수 등 변수화)
   * 정상 시나리오 로그와 침해사고(또는 모의해킹) 로그 레이블링(Labeling)
 * **11~12주차: 데이터셋 검증**
   * 학습용(Train), 검증용(Validation), 테스트용(Test) 데이터셋 분리 (통상 7:1.5:1.5)
   * 데이터 불균형(정상 로그 >>> 이상 로그) 해소를 위한 샘플링 전략 수립
### 🤖 4개월 차 (13~16주): AI 모델 개발 및 단체 검증
 * **13~14주차: AI 알고리즘 탐색 및 프로토타이핑**
   * 이상징후 탐지 알고리즘 구현 (Isolation Forest, Autoencoder, LSTM 등 성능 비교)
   * 지도학습(알려진 공격 탐지) 및 비지도학습(새로운 유형의 이상징후 탐지) 모델 설계
 * **15~16주차: 모델 학습 및 하이퍼파라미터 튜닝**
   * 정밀도(Precision), 재현율(Recall), F1-Score 기준 평가지표 설정
   * **보안 현업 관점의 오탐율(False Positive Rate) 최적화** (보안 관제 요원의 피로도 감소 목적)
### ⚙️ 5개월 차 (17~20주): 기존 시스템 연동 및 UI/UX 개발
 * **17~18주차: SIEM/SOAR 및 파이프라인 연동**
   * 개발된 AI 모델을 API 형태(Flask/FastAPI 등)로 패키징
   * 기존 SIEM(통합보안관제) 시스템에 AI 탐지 결과 데이터를 연동하는 파이프라인 구축
 * **19~20주차: 모니터링 대시보드 개발 및 통합 테스트**
   * 보안 요원이 AI 탐지 근거(Explainable AI 개념 적용)를 확인할 수 있는 대시보드 구현
   * 실시간 로그 유입 시 AI 추론 속도(Throughput) 및 부하 테스트 수행
### 🚀 6개월 차 (21~24주): 실환경 테스트, 안정화 및 이관
 * **21~22주차: 운영 환경 시범 적용 (Parallel Run)**
   * 기존 룰(Rule) 기반 관제 시스템과 AI 기반 시스템을 동시에 운영하며 결과 비교
   * 현업 피드백을 받아 오탐 룰셋 조정 및 모델 미세조정(Fine-tuning)
 * **23~24주차: 운영 이관 및 최종 보고**
   * 모델 주기적 재학습(Retraining) 프로세스 정립 및 자동화 시나리오 구성
   * 운영 매뉴얼 작성, 관제 인력 대상 교육 실시
   * 프로젝트 종료 보고 (성과 측정: 오탐 감소율, 탐지 시간 단축 등)
## ⚠️ 프로젝트 성공을 위한 핵심 체크포인트 (R&R)
 1. **데이터 품질 확보:** 보안 로그는 대량의 정상 로그 속에 아주 적은 이상 로그가 숨겨져 있습니다. 초기에 양질의 침해사고 데이터나 모의 훈련 데이터를 확보하는 것이 모델의 성패를 가릅니다.
 2. **개인정보보호 및 규제 준수:** 로그 내에 포함된 개인정보(식별자)를 개발 단계에서 어떻게 안전하게 처리(Masking/Anonymization)할 것인지에 대한 내부 보안성 심의를 1개월 차에 반드시 완료해야 합니다.
 3. **설명 가능한 AI (XAI):** AI가 "이 로그는 위험합니다"라고 했을 때, **왜 위험하다고 판단했는지(어떤 피처의 가중치가 높았는지)**를 대시보드에 보여주지 않으면 현업 관제 요원들이 신뢰하기 어렵습니다. 연동 단계에서 이 부분을 고려해야 합니다.
성공적인 프로젝트 추진을 응원합니다. 구체적인 로그 종류나 아키텍처에 대해 더 논의가 필요하시면 언제든 말씀해 주세요!


2026년 12월 완료를 목표로 하는 **AI 기반 보안 로그 점검 및 모니터링 프로젝트의 4단계 압축 일정표**입니다.
현재 시점(6월)부터 시작하여 올해 말까지 효율적으로 완료할 수 있도록 구성했습니다.
### 📅 AI 보안 로그 모니터링 프로젝트 4단계 일정 (6개월)
| 단계 | 주요 기간 | 핵심 추진 과제 | 주요 산출물 |
|---|---|---|---|
| **1단계: 기획 및 데이터 준비** | **6월 ~ 7월** | - 대상 로그 선정 및 표준화
- 인프라 및 가공 환경 구축
- **개인정보 비식별화 처리** 및 레이블링 | - 요구사항 정의서
- 데이터 전처리 파이프라인 |
| **2단계: AI 모델 개발 및 검증** | **8월 ~ 9월** | - 이상징후 탐지 알고리즘 설계
- 데이터셋 분리 및 모델 학습
- **오탐율(False Positive) 최적화** | - AI 모델 설계서
- 모델 성능 평가 보고서 |
| **3단계: 시스템 연동 및 UI 개발** | **10월 ~ 11월** | - AI 모델 API 패키징
- 기존 SIEM/SOAR 시스템 연동
- 설명 가능한 AI(XAI) 대시보드 구현 | - 시스템 연동 규격서
- 모니터링 대시보드 화면 |
| **4단계: 시범 운영 및 이관** | **12월** | - 실환경 시범 운영 (Parallel Run)
- 모델 미세조정 및 재학습 프로세스 정립
- 최종 운영 이관 및 교육 완료 | - 최종 완료 보고서
- 운영 매뉴얼 |
### 💡 단계별 핵심 성공 요인 (Quick Check)
 * **1단계 (데이터):** 로그 내 개인정보 마스킹을 초기에 완벽히 정립해야 법적 리스크를 방지할 수 있습니다.
 * **2단계 (모델):** 보안 관제 요원의 피로도를 줄이기 위해 '오탐 분별력'을 높이는 데 초점을 맞춥니다.
 * **3단계 (연동):** 실시간 로그 인입 시 AI 추론 속도가 지연되지 않도록 아키텍처 최적화가 필요합니다.
 * **4단계 (이관):** 프로젝트 종료 후에도 모델이 최신 공격 트렌드를 반영할 수 있도록 자동 재학습 구조를 넘겨주어야 합니다.



**접근 로그(Access Log)** 분석에만 집중하여 범위를 대폭 축소한, 실현 가능성이 높은 4단계 일정표입니다.
불필요한 이기종 장비 연동을 제외하고 **'비정상 접근 시도 탐지(UBA/이상징후)'**에만 초점을 맞추어 12월까지 완료하는 일정입니다.
### 📅 AI 기반 접근 로그 분석 프로젝트 일정표 (12월 완료)
| 단계 | 주요 기간 | 핵심 추진 과제 | 주요 산출물 |
|---|---|---|---|
| **1단계: 로그 수집 및 전처리** | **6월 ~ 7월** | - 분석 대상 선정 (시스템/웹 서버/DB 접근 로그 중 택1)
- 계정명, IP 등 **개인정보 비식별화(마스킹)**
- 시간별/계정별 접근 빈도 등 AI 학습용 피처 추출 | - 접근 로그 정의서
- 데이터 정제 스크립트 |
| **2단계: AI 모델 학습** | **8월 ~ 9월** | - 이상 접근 탐지 알고리즘 적용 (Isolation Forest 등)
- 평소와 다른 시간/장소(IP)에서의 접근 패턴 학습
- 업무 외 시간 대량 접근 등 오탐/미탐 튜닝 | - AI 분석 모델 (Lightweight)
- 모델 탐지 성능 결과서 |
| **3단계: 간단한 대시보드 연동** | **10월 ~ 11월** | - AI 모델을 API(Flask/FastAPI 등)로 경량화
- 실시간/주기적 접근 로그 입력 파이프라인 연결
- **경고 알림 및 이상 접근 사유 시각화 페이지** 구현 | - API 연동 규격서
- 모니터링 웹 화면 (Streamlit 등) |
| **4단계: 검증 및 운영 이관** | **12월** | - 실환경 로그 주입을 통한 탐지 정확도 최종 검증
- 실제 관제/운영자 피드백 반영 및 룰 보완
- 주기적인 신규 접근 패턴 재학습 가이드 마련 | - 최종 완료 보고서
- 간단한 운영 매뉴얼 |
### 💡 프로젝트 압축 포인트
 * **범위 최소화:** 방화벽이나 IDS 같은 복잡한 보안 장비 대신, **'누가, 언제, 어디서, 무엇에 접근했는가'**가 담긴 단일 포맷의 접근 로그만 다룹니다.
 * **학습 단순화:** 복잡한 딥러닝 대신 비지도학습 알고리즘(Isolation Forest, 단일 클래스 SVM 등)을 활용해 **"평소와 다른 접근"**을 빠르게 찾아내는 데 집중합니다.


최고의 정보보안 기술 전문 컨설턴트로서, **접근 로그(Access Log) 기반의 AI 이상징후 탐지 및 공격 예방 시스템**을 성공적으로 가동하기 위한 핵심 프롬프트 세트를 제안합니다.
이 프롬프트들은 LLM 또는 AI 에이전트가 데이터 엔지니어, 보안 분석가, 대응 전문가의 역할을 정밀하게 수행하도록 설계되었습니다. 프로젝트의 각 단계(수집/전처리, 분석/탐지, 예방/대응)에 맞춰 복사하여 사용하실 수 있습니다.
## 🛠️ 1단계: 데이터 전처리 및 개인정보 비식별화 프롬프트
> **목적:** 수집된 원본 접근 로그를 분석 가능한 형태로 파싱하고, 법적 리스크(개인정보보호법 등)를 방지하기 위해 민감 정보를 안전하게 마스킹합니다.
> 
```markdown
[Role]
너는 최고의 정보보안 데이터 엔지니어다. raw 접근 로그를 분석 최적화 형태로 전처리하고 비식별화하는 임무를 맡았다.

[Input Data]
- 입력 데이터: [여기에 raw 접근 로그 샘플 또는 포맷 삽입, 예: 웹서버, DB, 또는 시스템 접근 로그]

[Task Instructions]
1. 로그 파싱: 제공된 raw 로그를 분석하기 좋게 [JSON 또는 CSV] 구조로 파싱해라. (Timestamp, Source IP, User ID, Access Action, Status Code, Resource 등)
2. 개인정보 비식별화 (필수):
   - User ID(계정명): 앞 3자리만 남기고 뒤는 마스킹 처리 (예: admin123 -> adm*****).
   - Source IP: C클래스 혹은 D클래스 대역을 마스킹 처리 (예: 192.168.1.50 -> 192.168.1.***).
3. 피처 엔지니어링 추천: AI 이상징후 탐지 모델(예: Isolation Forest)이 학습하기 좋은 형태로, 시간대별 접근 빈도(Hourly Frequency), 동일 IP의 실패 횟수(Failed Attempts) 등의 파생 변수를 생성하는 Python 코드를 작성해라.

[Output Format]
- 파싱 및 마스킹 완료된 데이터 예시 (JSON 포맷)
- 파라미터 추출 및 비식별화를 수행하는 Python 전처리 스크립트 코드

```
## 🔍 2단계: AI 이상징후 분석 및 컨텍스트 추론 프롬프트
> **목적:** 전처리된 로그를 바탕으로 '평소와 다른 패턴'을 탐지하고, 단순한 룰 기반이 아닌 공격의 맥락(Context)을 분석합니다.
> 
```markdown
[Role]
너는 숙련된 AI 기반 보안관제 실무 전문가(Tier 3 Analyst)다. 전처리된 접근 로그 데이터를 분석하여 단순 오탐(False Positive)을 걸러내고, 실제 위협인 이상징후를 탐지해야 한다.

[Analysis Context]
- 정상 패턴 기준: 임직원들은 주로 평일 09:00~18:00에 국내 IP로 접근하며, 일평균 실패 횟수는 3회 미만임.

[Input Data]
- 이상 데이터 후보: [여기에 1단계에서 전처리된 이상징후 탐지 로그 데이터 삽입]

[Task Instructions]
다음 로그 데이터를 보고 아래 관점에서 공격 유무를 분석하라:
1. 위험도 점수 산정: 1~10점 사이의 위험도를 부여하고 그 이유를 설명하라.
2. 공격 시나리오 추론: 무차별 대입 공격(Brute Force), 크레덴셜 스터핑(Credential Stuffing), 권한 상승(Privilege Escalation), 비인가 지역/시간대 접근 등 어떤 공격 유형에 가까운지 분석하라.
3. 오탐 판단: 만약 이것이 정상적인 야간 작업이나 개발자의 테스트 환경 접근일 가능성이 있다면, 어떤 추가 데이터(예: 작업 결재 이력)를 확인해야 오탐을 확정할 수 있는지 기술하라.

[Output Format]
- 위험도: [점수]
- 공격 유형: [추론된 공격 명칭]
- 탐지 근거(Explainable AI): (현업 보안 요원이 이해할 수 있도록 명확한 텍스트로 설명)

```
## 🛡️ 3단계: 공격 예방 및 대응(SOAR 연동) 프롬프트
> **목적:** 탐지된 위협이 실제 피해로 이어지기 전에, 시스템이 자동으로 방어 조치를 취하거나 보안 관리자에게 즉각적인 예방 가이드를 제공하도록 합니다.
> 
```markdown
[Role]
너는 침해사고 대응(CERT) 및 보안 아키텍처 전문가다. AI가 찾아낸 이상 접근 위협에 대해 피해를 최소화하고 향후 공격을 원천 차단하기 위한 예방 및 대응 플레이북을 생성하라.

[Threat Scenario]
- 탐지된 위협: [2단계에서 도출된 위협 분석 결과 입력, 예: 해외 비인가 IP를 통한 관리자 계정 다중 로그인 실패 및 성공]

[Task Instructions]
1. 즉각적인 차단 조치(Containment): SOAR(보안 편성 및 자동 대응) 시스템과 연동하여 자동으로 실행할 수 있는 방어 명령(API 호출, 방화벽 IP 차단 정책, 세션 강제 종료 등)을 제시하라.
2. 근본적 예방 대책(Hardening): 동일한 취약점으로 인한 재발을 막기 위해 해당 접근 로그 대상 시스템(서버/DB)에 적용해야 할 보안 강화 정책(예: MFA 필수화, IP 화이트리스트 지정, 패스워드 정책 강화)을 가이드하라.
3. 관리자 알림 메시지: 보안 담당자가 Slack이나 SMS로 받아보고 즉시 상황을 파악할 수 있는 3줄 요약 경고 문구를 작성하라.

[Output Format]
- [Immediate Action] 자동 차단 스크립트 가이드 (CLI 명령어 또는 API 가이드)
- [Prevention Strategy] 시스템 보안 강화 권고 사항
- [Alert Message] 담당자 전송용 요약 문구

```
### 💡 컨턴설턴트의 활용 팁
 * **파이프라인 자동화:** 위 프롬프트들을 **LangChain**이나 **FastAPI** 기반의 백엔드 시스템에 API 형태로 임베딩하면, 로그 수집부터 대응까지 한 흐름으로 이어지는 **자동화된 AI 보안 비서 서비스**를 구축할 수 있습니다.
 * **대시보드 시각화:** 2단계의 '탐지 근거' 출력을 **Streamlit** 대시보드 화면에 그대로 연동하면, 관제 요원이 AI의 판단 이유를 한눈에 모니터링할 수 있어 오탐 정제 업무가 획기적으로 줄어듭니다.


정보보안 컨설턴트로서, 앞서 설계한 **4단계 접근 로그 분석 프로젝트**를 실제로 가동할 수 있는 **Flask 및 SQLite 기반의 프로토타입 시스템**을 구현했습니다.
이 코드는 단일 파일(app.py)로 가동할 수 있으며, 데이터 엔지니어링(수집/비식별화), AI 기반 분석(Isolation Forest 활용), 그리고 대시보드 시각화까지 하나의 파이프라인으로 연결되어 있습니다.
## 🏗️ AI 접근 로그 모니터링 시스템 아키텍처 및 구현
이 시스템은 SQLite에 원본 로그를 적재한 뒤, 파이썬의 scikit-learn 라이브러리를 이용해 평소와 다른 **이상 접근 패턴(시간대, 실패 횟수 기반)**을 탐지하여 대시보드에 시각화합니다.
### 1. 환경 설정 (필수 패키지 설치)
터미널에서 아래 명령어를 실행하여 필요한 라이브러리를 설치합니다.
```bash
pip install Flask scikit-learn pandas numpy

```
### 2. 전체 소스 코드 (app.py)
```python
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

```
## 💡 코드에 적용된 정보보안 핵심 컨설팅 포인트
 1. **비지도학습(Isolation Forest) 선정 이유:** 보안 로그의 특성상 '공격 로그'보다는 '정상 로그'가 압도적으로 많습니다. 이 코드는 정상 패턴을 스스로 학습한 뒤, 거기서 멀리 떨어진(예: 새벽 3시에 실패 횟수가 20회인 로그) 데이터를 **이상징후(Anomaly)**로 자동 분류합니다.
 2. **개인정보 비식별화 아키텍처 (1단계 반영):**
   masking_id 및 masking_ip 함수를 통해 웹 대시보드 화면에 노출될 때 계정명과 IP 주소 뒷자리를 자동으로 마스킹 처리하여 **내부 인력에 의한 2차 개인정보 유출 리스크를 원천 차단**했습니다.
 3. **실시간 시뮬레이션 환경 탑재:**
   상단 양식에 평범한 데이터(ex: user_a, 192.168.1.15, 실패 0, 유지 100)를 넣으면 **정상(녹색)**으로 분류되지만, 비정상적 데이터(ex: 야간 시간대, 실패 50회 등)를 주입하면 AI가 즉시 분석하여 **위협(주황색)** 라인으로 격리 표시합니다.
### 🏃‍♂️ 실행 방법
 1. 위 코드를 app.py로 저장합니다.
 2. 터미널에서 python app.py를 실행합니다.
 3. 브라우저에서 http://127.0.0.1:5000에 접속하여 대시보드를 확인하고 테스트해 보세요.
