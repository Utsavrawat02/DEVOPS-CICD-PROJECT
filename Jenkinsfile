pipeline {
    agent any

    environment {
        IMAGE = 'calc-app:dev'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t ${IMAGE} .'
            }
        }

        stage('Smoke test') {
            steps {
                sh 'docker run --rm ${IMAGE} python app.py health'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    mkdir -p reports
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${IMAGE} \
                        flake8 app.py calculator.py --output-file=/app/reports/flake8.txt
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${IMAGE} \
                        pytest --junitxml=/app/reports/test-results.xml
                '''
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${IMAGE} \
                        pytest --cov=. --cov-report=xml:/app/reports/coverage.xml --cov-report=html:/app/reports/htmlcov
                '''
            }
        }

        stage('Security scan') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${IMAGE} \
                        bandit -r . -f sarif -o /app/reports/bandit.sarif
                '''
            }
        }

        stage('Archive & publish') {
            steps {
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            junit 'reports/test-results.xml'
            publishHTML(target: [
                reportDir: 'reports/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
        }
    }
}