pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<your-username>/qa-automation-framework.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && playwright install --with-deps chromium'
            }
        }

        stage('Run Smoke Tests') {
            steps {
                sh '. venv/bin/activate && pytest -m smoke'
            }
        }

        stage('Run Full Regression Suite') {
            steps {
                sh '. venv/bin/activate && pytest -m "ui or api" -n auto'
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Automation Test Report'
            ])
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
