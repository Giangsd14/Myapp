import uvicorn
from myapp.main import app

if __name__ == '__main__':
	uvicorn.run(app, host='127.0.0.1', port=8000)

# 	netstat -ano | findstr :8000
# 	taskkill /IM uvicorn.exe /F