DevOps CI/CD Project

Overview
This project demonstrates a complete DevOps CI/CD workflow using Docker, GitHub, and automation tools.
<!-- Build Docker Images  -->
1) For Development and Testing
docker build -t calc-app:prod -f docker/Dockerfile.prod .   
2) For Production And Deployment
docker build -t calc-app:dev -f docker/Dockerfile.prod .  

Powershell Commands to run the Docker Tests

docker run --rm calc-app:prod python app.py health                      

docker run --rm `
 calc-app:dev `
 python app.py add 2 3
 
docker run --rm `                  
-v "${PWD}/reports:/app/reports" `
calc-app:dev `
bandit -r . -f sarif -o ./reports/bandit.sarif

docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 flake8 app.py calculator.py > reports/linter.txt

 docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 pytest --junitxml=/app/reports/test-results.xml


 docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 python -m pytest --cov=. --cov-report=xml:/app/reports/coverage.xml tests/

 

docker run -d --name jenkins `
  --network jenkins `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  jenkins/jenkins:lts