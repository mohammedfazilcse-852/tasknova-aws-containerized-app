# TaskNova — Personal Productivity Command Center

A Flask-based task manager with a responsive dark SaaS dashboard and MySQL persistence.

## Features
- Create, list, complete/uncomplete, and delete tasks
- Productivity summary and completion progress
- MySQL database configuration through environment variables
- `/health` endpoint for load-balancer/container health checks
- Docker-ready; intended for Amazon ECR and ECS Fargate

## Existing database
This project expects the existing `tododb.tasks` table:

```sql
CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Run locally
1. Create a virtual environment and install packages:
   `python -m venv .venv`
   Windows: `.venv\\Scripts\\activate`
   Linux/macOS: `source .venv/bin/activate`
   `pip install -r requirements.txt`
2. Set the environment variables shown in `.env.example` in your terminal. Do not commit real credentials.
3. Start the app: `python app.py`
4. Open `http://localhost:5000` and test `http://localhost:5000/health`.

## Build container
`docker build -t tasknova:1.0 .`

Run with environment variables supplied securely at runtime:
`docker run --rm -p 5000:5000 -e DB_HOST=... -e DB_PORT=3306 -e DB_USER=... -e DB_PASSWORD=... -e DB_NAME=tododb tasknova:1.0`

For ECS, inject the database password from AWS Secrets Manager in the task definition. Never bake credentials into the image or commit them to Git.
