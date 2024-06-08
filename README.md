# ester2orca

Python server to transfer info about books from ester.com to api

```
docker build -t ester2orca .
docker run -d -p 8000:8000 ester2orca
npm install ngrok -g
ngrok config add-authtoken ...
ngrok http 8000
```
