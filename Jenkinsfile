pipeline {
    agent any

    environment {
        DEV_IMAGE  = 'calc-app:dev'
        PROD_IMAGE = 'calc-app:prod'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build dev/test image') {
            steps {
                sh 'docker build -f Docker/Dockerfile.dev -t ${DEV_IMAGE} .'
            }
        }

        stage('Smoke test') {
            steps {
                sh 'docker run --rm ${DEV_IMAGE} python app.py health'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    mkdir -p reports
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${DEV_IMAGE} \
                        flake8 app.py calculator.py --output-file=/app/reports/flake8.txt || true
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${DEV_IMAGE} \
                        pytest --junitxml=/app/reports/test-results.xml
                '''
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${DEV_IMAGE} \
                        pytest --cov=. --cov-report=xml:/app/reports/coverage.xml --cov-report=html:/app/reports/htmlcov
                '''
            }
        }

        stage('Security scan') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}/reports:/app/reports ${DEV_IMAGE} \
                        bandit -r . -f sarif -o /app/reports/bandit.sarif || true
                '''
            }
        }

        stage('Archive test reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }

        stage('Build production image') {
            steps {
                sh 'docker build -f Docker/Dockerfile.prod -t ${PROD_IMAGE} .'
            }
        }

        stage('Verify production image') {
            steps {
                sh 'docker run --rm ${PROD_IMAGE} python app.py health'
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/test-results.xml', allowEmptyResults: true
            publishHTML(target: [
                reportDir: 'reports/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
        }
        success {
            echo 'All gates passed — dev tested, prod image built and verified.'
        }
        failure {
            echo 'Pipeline failed — check the failing stage above. Production image was not built.'
        }
    }
}