# Hostel-Visitor-Register
| Team | Partner 1 | Partner 2 | Partner 3| Project | Live App |
|---|---|---|---|---|---|
| 4 | Praneeth | Fayaz | Pavan Kumar|[Hostel-Visitor-Register](https://github.com/praneethreddy1904/Hostel-Vistor-Register/edit/main/README.md) | http://13.232.121.64:8001/docs |

# Backend Setup and Execution

Open a terminal and navigate to the backend folder.

cd backend

### Create Virtual Environment

python -m venv venv

### Activate Virtual Environment

Windows:

venv\Scripts\activate

### Install libraries
pip install fastapi
            pydantic 
            sqlalchemy 
            pyjwt 
            argon2-cffi 
            uvicorn

### Install Dependencies

pip install -r requirements.txt

### Run Backend

uvicorn main:app --reload --port 8001

Backend URL:

http://127.0.0.1:8001

## 7. Frontend Setup and Execution

Open another terminal.

Navigate to the frontend folder.

cd frontend

### Install Dependencies

npm install

npm create vite@latest -- --template react 

### Run Frontend

npm run dev

Frontend URL:

http://localhost:5173

## 8. Docker Setup and Execution

### Build Docker Image

docker build -t project-name .

### Run Docker Container

docker run -d -p 8001:8001 --name project-container project-name

### Check Running Containers

docker ps

### Stop Container

docker stop project-container

### start container

docker start project-container

### Remove Container

docker rm project-container

API Documentation:

http://127.0.0.1:8001/docs

##  API Requirements

The application must provide APIs for the following. Fill in the API contract for each row.

| # | Description | Method | Endpoint | Request Body | Status Codes |
| --- | --- | --- | --- | --- | --- |
| A1 | Register a new hostel staff user | POST | /register |{ "username", "email", "password" } | 201 created |
| A2 | Login and generate JWT access and refresh tokens | POST| /Login |{ "email", "password" } | 200 ok |
| A3 | Generate a new access token using a refresh token | POST | /refresh |None (refresh token sent in the refresh_token header) | 200 ok |
| E1 | Get all visitor records registered by the logged-in staff member | GET | /visitors | None (access token sent in the token header) | 200 ok |
| E2 | Register a new visitor and associate the record with the logged-in staff member | POST | /visitors |{"visitor_name","student_name","room_no","purpose","visit_date"}| 201 created |

## Datebase Tables

| # | Table | Columns |
| --- | --- | --- |
| 1 | users | `id`, `username`, `email`, `hashed_password`, `created_at` |
| 2 | visitors | `id`, `user_id`, `visitor_name`, `student_name`, `room_no`, `purpose` , `visit_date` , `created_at` |
