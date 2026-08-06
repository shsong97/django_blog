# django_blog

Django 4.2 기반 블로그 / 투표 / 사용자 관리 예제 프로젝트입니다.

## 요구 사항

- Python 3.10+
- Django 4.2 LTS

## 로컬 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

기본 DB는 SQLite(`db.sqlite3`)입니다.

- PostgreSQL을 쓰려면 `DATABASE_URL` 또는 `USE_POSTGRES=1` 환경변수를 설정하세요.
- 메일 설정은 환경변수(`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` 등)를 사용하세요.
  로컬용 `credentials.json`이 있으면 그 값을 읽어옵니다(저장소에 커밋하지 마세요).

## 테스트

```bash
python manage.py test polls mysite
```

## 배포

`Procfile`은 gunicorn 기준입니다.

```bash
web: gunicorn mysite.wsgi
```

정적 파일은 WhiteNoise로 서빙합니다.
