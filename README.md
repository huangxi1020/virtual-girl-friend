### TL;DR
```shell
pip install -r requirements.txt
python api.py
```

### Use a venv:
```shell
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Call
```curl
curl --location 'http://127.0.0.1:8888/chat_with_girlfriend' \
--header 'Content-Type: application/json' \
--data '{
    "message": "早上好"
}'
```