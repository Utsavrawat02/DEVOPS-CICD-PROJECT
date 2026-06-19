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
                    docker rm -f lint_run 2>/dev/null || true
                    docker create --name lint_run ${DEV_IMAGE} \
                        flake8 app.py calculator.py --output-file=/app/reports/flake8.txt
                    docker start -a lint_run 
                    docker cp lint_run:/app/reports/flake8.txt reports/flake8.txt 
                    docker rm lint_run  
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    docker rm -f unit_test_run 2>/dev/null || true 
                    docker create --name unit_test_run ${DEV_IMAGE} \
                        pytest --junitxml=/app/reports/test-results.xml
                    docker start -a unit_test_run
                    docker cp unit_test_run:/app/reports/test-results.xml reports/test-results.xml
                    docker rm unit_test_run
                '''
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    docker rm -f coverage_run 2>/dev/null || true
                    docker create --name coverage_run ${DEV_IMAGE} \
                        pytest --cov=. --cov-fail-under=80 \
                        --cov-report=xml:/app/reports/coverage.xml \
                        --cov-report=html:/app/reports/htmlcov
                    docker start -a coverage_run
                    docker cp coverage_run:/app/reports/coverage.xml reports/coverage.xml
                    docker cp coverage_run:/app/reports/htmlcov reports/htmlcov
                    docker rm coverage_run
                '''
            }
        }

        stage('Security scan') {
            steps {
                sh '''
                    docker rm -f security_run 2>/dev/null || true
                    docker create --name security_run ${DEV_IMAGE} \
                        bandit -r . -ll -f sarif -o /app/reports/bandit.sarif
                    docker start -a security_run 
                    docker cp security_run:/app/reports/bandit.sarif reports/bandit.sarif 
                    docker rm security_run
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