# KOBIS 박스오피스 대시보드

Streamlit으로 만든 영화 박스오피스 대시보드입니다.  
날짜를 선택하면 영화진흥위원회(KOBIS) Open API에서 해당 날짜의 박스오피스 데이터를 가져와 아래 내용을 보여줍니다.

- 1~10위 영화의 당일 관객 수 막대그래프
- 박스오피스 상세 데이터 표

이 문서는 로컬 실행과 Streamlit Community Cloud 배포를 처음 해보는 사람 기준으로 작성했습니다.

## 1. 준비물

아래 3가지가 필요합니다.

- Python 3.11 이상
- `uv`
- KOBIS API 키

## 2. Python 설치 확인

터미널에서 아래 명령어를 실행하세요.

```bash
python3 --version
```

예시:

```bash
Python 3.11.8
```

`command not found`가 나오면 Python이 아직 설치되지 않은 상태입니다.

## 3. uv 설치

macOS 또는 Linux에서는 보통 아래 명령어로 설치합니다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 확인:

```bash
uv --version
```

## 4. KOBIS API 키 준비

영화진흥위원회 Open API에서 본인 API 키를 발급받아야 합니다.

대시보드는 아래 두 방식 중 하나로 키를 읽습니다.

1. `st.secrets`의 `KOBIS_API_KEY`
2. `app.py` 안의 `API_KEY`

로컬 테스트만 할 때는 `app.py`에 직접 넣어도 됩니다.  
하지만 GitHub에 올리거나 배포할 때는 `st.secrets`를 쓰는 편이 안전합니다.

## 5. 프로젝트 폴더로 이동

```bash
cd /Users/codepark/codex-project1/codex_practice/kobis-dashboard
```

## 6. 로컬 실행 방법

### 방법 A. 가장 쉬운 방식: `app.py`에 키 넣기

`app.py`에서 아래 코드를 찾으세요.

```python
API_KEY = "여기에_KOBIS_API_KEY를_입력하세요"
```

그리고 실제 키로 바꾸세요.

```python
API_KEY = "본인_KOBIS_API_키"
```

### 방법 B. 더 안전한 방식: 로컬 secret 파일 사용

프로젝트 폴더 안에 `.streamlit/secrets.toml` 파일을 만들고 아래처럼 입력하세요.

```toml
KOBIS_API_KEY = "본인_KOBIS_API_키"
```

이 파일은 `.gitignore`에 포함되어 있어서 GitHub에 올라가지 않도록 설정해 두었습니다.

## 7. 필요한 패키지 설치

```bash
uv sync
```

설치되는 주요 라이브러리:

- `streamlit`
- `pandas`
- `requests`

## 8. 로컬에서 앱 실행

```bash
uv run streamlit run app.py
```

정상 실행되면 보통 아래와 비슷한 주소가 보입니다.

```bash
Local URL: http://localhost:8501
```

브라우저에서 그 주소를 열면 됩니다.

## 9. 앱 사용 방법

1. 날짜를 선택합니다.
2. 선택한 날짜의 KOBIS 박스오피스 데이터를 불러옵니다.
3. 상단에서 조회 날짜, 1위 영화, 1위 관객 수를 확인합니다.
4. 막대그래프에서 1~10위 영화 관객 수를 확인합니다.
5. 아래 표에서 순위, 영화명, 누적 관객 수, 매출액, 개봉일 등을 봅니다.

## 10. Streamlit Community Cloud로 배포하기

2026-03-18 기준으로 Streamlit Community Cloud는 무료로 사용할 수 있습니다.  
현재 이 프로젝트는 Community Cloud에 올릴 수 있게 필요한 파일을 이미 갖춘 상태입니다.

배포 전 준비된 파일:

- `app.py`
- `requirements.txt`
- `pyproject.toml`
- `.streamlit/config.toml`

### 1) GitHub 저장소 만들기

먼저 이 프로젝트를 GitHub 저장소에 올려야 합니다.

필수 조건:

- GitHub 계정
- 이 프로젝트가 들어 있는 GitHub 저장소

공개 저장소로 올릴 경우 `app.py`에 API 키를 직접 넣으면 안 됩니다.  
배포 환경에서는 반드시 Streamlit secrets를 쓰는 것을 권장합니다.

### 2) GitHub에 코드 업로드

예시 명령어:

```bash
git init
git add .
git commit -m "Add KOBIS Streamlit dashboard"
```

그 다음 GitHub에서 새 저장소를 만든 뒤 연결해서 push 합니다.

예시:

```bash
git remote add origin <본인_저장소_URL>
git branch -M main
git push -u origin main
```

### 3) Streamlit Community Cloud 접속

아래 페이지로 이동하세요.

- https://share.streamlit.io/

또는 최신 안내 문서를 참고하세요.

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

### 4) GitHub 저장소 연결

배포 화면에서 아래 정보를 선택합니다.

- Repository: 방금 올린 GitHub 저장소
- Branch: `main`
- Main file path: `app.py`

### 5) 배포용 Secret 등록

배포 설정의 Secrets 항목에 아래 내용을 넣으세요.

```toml
KOBIS_API_KEY = "본인_KOBIS_API_키"
```

이 방식이 가장 안전합니다.

### 6) Deploy 버튼 클릭

배포가 끝나면 `https://...streamlit.app` 형태의 주소가 발급됩니다.

## 11. 배포 후 수정 사항 반영

GitHub에 코드를 다시 push 하면 Streamlit Community Cloud에서 자동으로 다시 배포됩니다.

즉, 수정 흐름은 보통 아래와 같습니다.

1. 로컬에서 코드 수정
2. GitHub에 commit / push
3. Streamlit Cloud가 자동 재배포

## 12. 자주 발생하는 문제

### 1) API 키 오류

증상:

- 앱이 시작되자마자 경고가 뜸
- 데이터가 로드되지 않음

확인:

- `app.py`의 `API_KEY`를 제대로 넣었는지
- 또는 `secrets.toml` / Streamlit secrets에 `KOBIS_API_KEY`가 들어 있는지

### 2) 데이터가 없다고 나옴

증상:

- "해당 날짜의 박스오피스 데이터가 없습니다." 메시지 출력

원인:

- 아직 집계되지 않은 날짜일 수 있음

팁:

- 전날 날짜로 먼저 테스트해 보세요.

### 3) `uv`가 동작하지 않음

증상:

- `uv: command not found`

해결:

- 설치 후 터미널을 다시 열기
- `uv --version`으로 재확인

### 4) 배포는 됐는데 앱에서 에러가 남

확인 순서:

1. Streamlit Cloud의 Secrets에 `KOBIS_API_KEY`를 넣었는지 확인
2. Main file path가 `app.py`인지 확인
3. GitHub 저장소에 필요한 파일이 모두 올라갔는지 확인

## 13. 파일 설명

- `app.py`: 메인 Streamlit 앱
- `pyproject.toml`: 프로젝트 의존성 정의
- `requirements.txt`: 배포 플랫폼 호환성을 위한 의존성 파일
- `.streamlit/config.toml`: Streamlit 설정 파일
- `README.md`: 실행 및 배포 가이드

## 14. 빠른 실행 요약

로컬 실행:

```bash
cd /Users/codepark/codex-project1/codex_practice/kobis-dashboard
uv sync
uv run streamlit run app.py
```

배포 요약:

1. GitHub에 코드 업로드
2. Streamlit Community Cloud에서 저장소 연결
3. `KOBIS_API_KEY`를 Secrets에 등록
4. `app.py`를 메인 파일로 지정해서 배포
