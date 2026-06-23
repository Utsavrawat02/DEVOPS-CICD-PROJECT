DevOps CI/CD Project

Project Overview
This project demonstrates a complete DevOps CI/CD workflow using Docker, GitHub, and jenkins for automation tools.this involves building a local CI/CD pipeline for a Python calculator app, using Docker and Jenkins. Every code change is automatically built, smoke-tested, linted, unit-tested, coverage-checked, and security-scanned. Passing builds produce a separate, minimal production image. Demonstrates real-world DevOps practices: quality gates, containerization, and automated, repeatable software delivery.
This is not just a Python assignment. The deliverable is a complete, repeatable CI/CD workflow that another engineer could clone and adapt for a client project.

python version : 3.10.11

<!-- App Usage -->
python app.py health 
output -> ok 
python app.py <function> <v1> <v2>
function -> add ,mul, sub, div

where v1 and v2 are numbers 
incase of string if string can be converted to integer then operation is performed else it will throw an error
output -> some integer based on your function and value
ie 
python app.py sub 23 34
output -> 57

<!-- Build Docker Images  -->
1) For Development and Testing
docker build -t devops-cicd-project:test -f docker/Dockerfile.prod .   
2) For Production And Deployment
docker build -t devops-cicd-project:dev -f docker/Dockerfile.prod .  

<!-- Powershell Commands to run the Docker Tests -->

docker run --rm calc-app:prod python app.py health                      

docker run --rm `
 calc-app:dev `
 python app.py add 2 3

docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 flake8 app.py calculator.py > reports/linter.txt

 docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 bandit -r . -f sarif -o ./reports/bandit.sarif
 
 docker run --rm `
 -v "${PWD}/reports:/app/reports" `
 calc-app:dev `
 python -m pytest --cov=. --cov-report=xml:/app/reports/coverage.xml tests/

docker network create jenkins

docker run -d --name jenkins `
  --network jenkins `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  jenkins/jenkins:lts



<!-- Git bash Commands for running Docker-->

docker run --rm devops-cicd-project:test

docker run --rm devops-cicd-project:test python app.py add 4 6

docker run --rm -v "$(pwd)/reports:/app/reports" devops-cicd-project:test  python -m pytest tests/

docker run --rm -v "$(pwd)/reports:/app/reports" devops-cicd-project:test  python -m pytest --junitxml=/app/reports/test-results.xml tests/

docker run --rm -v $(pwd)/reports:/app/reports devops-cicd-project:test python -m pytest --cov=. --cov-report=xml:/app/reports/coverage.xml tests/

docker run --rm -v "$(pwd)/reports:/app/reports" devops-cicd-project:test flake8 app.py calculator.py > reports/linter.txt

docker run --rm -v "$(pwd)/reports:/app/reports" devops-cicd-project:test bandit -r . -f sarif -o ./reports/bandit.sarif

docker network create jenkins~

docker run -d --name jenkins --network jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -u root jenkins/jenkins:lts