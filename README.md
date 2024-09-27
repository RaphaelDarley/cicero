# team-apex
The repo for Team Apex in the Summer 2024 AI Json hackathon\
got to: https://cicero.darley.dev/api/basic to try out the api\
![Logo_with_text](https://github.com/user-attachments/assets/8457888f-4f29-4bbd-a12a-9d715234a883)

frontend: npm run dev -- --port 8812 --host
db: surreal start --bind 127.0.0.1:8001 rocksdb://cicero.db
backend: (poetry shell) fastapi run --port 8811 server.py