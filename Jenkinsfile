pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DATABASE_URL = credentials('backend-database-url')
        JWT_SECRET = credentials('backend-jwt-secret')
        CORS_ORIGINS = 'http://localhost:8080,http://127.0.0.1:8080'
        FRONTEND_URL = 'http://localhost:8080'
        STRIPE_SECRET_KEY = ''
        STRIPE_WEBHOOK_SECRET = ''
        GOOGLE_CLIENT_IDS = ''
        SUPABASE_URL = ''
        SUPABASE_ANON_KEY = ''
        DIRECT_URL = ''
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Python') {
            steps {
                dir('backend') {
                    bat 'py -m venv .venv'
                    bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                    bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
                }
            }
        }

        stage('Static Validation') {
            steps {
                dir('backend') {
                    bat '.venv\\Scripts\\python -m compileall app main.py'
                    bat '.venv\\Scripts\\python -c "from app.main import app; print(app.title)"'
                }
            }
        }

        stage('Health Smoke Test') {
            steps {
                dir('backend') {
                    bat '.venv\\Scripts\\python -c "from app.main import health; response = health(); assert response[''success''] is True; assert response[''data''][''status''] == ''ok''; print(response)"'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente.'
        }
        failure {
            echo 'Pipeline fallido. Revisa la consola de Jenkins.'
        }
    }
}
