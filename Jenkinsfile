pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
        JWT_SECRET = 'test_secret'
        JWT_ALGORITHM = 'HS256'
        JWT_EXPIRES_MINUTES = '10080'
        CORS_ORIGINS = 'http://localhost:8080'
        FRONTEND_URL = 'http://localhost:8080'
    }

    stages {
        stage('Inicio') {
            steps {
                echo 'Empieza la pipeline de Jenkins'
            }
        }

        stage('Ver archivos') {
            steps {
                bat 'dir'
            }
        }

        stage('Crear entorno virtual') {
            steps {
                bat '''
                py -3.11 -m venv .venv
                .venv\\Scripts\\python -m pip install --upgrade pip
                '''
            }
        }

        stage('Instalar dependencias') {
            steps {
                bat '''
                .venv\\Scripts\\python -m pip install -r requirements.txt
                .venv\\Scripts\\python -m pip install pytest httpx pytest-cov
                '''
            }
        }

        stage('Comprobar sintaxis') {
            steps {
                bat '.venv\\Scripts\\python -m compileall app main.py'
            }
        }

        stage('Ejecutar tests') {
            steps {
                bat '.venv\\Scripts\\python -m pytest -q'
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminada correctamente'
        }
        failure {
            echo 'La pipeline ha fallado'
        }
    }
}
