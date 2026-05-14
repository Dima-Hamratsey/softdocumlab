# Lab 4: Strategy (API -> Console/File/Kafka/Redis)

## Commands
```powershell
pip install -r requirements.txt
docker compose up -d
python main.py
```

## Read output

### File
```powershell
Get-Content .\lab4_output.json
```

### Redis
```powershell
docker compose exec redis redis-cli
```
Then run inside redis-cli:
```
LRANGE lab4:output 0 -1
```

### Kafka
```powershell
docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic lab4_output --from-beginning
```

## Notes
- The reader keeps 7 fields and limits output to 100 items.
