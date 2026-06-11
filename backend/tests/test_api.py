import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_upload_dummy():
    files = {'file': ('test.txt', b'hello world')}
    r = client.post('/upload', files=files)
    assert r.status_code == 200
    j = r.json()
    assert j.get('filename') == 'test.txt'
