pipeline {
    agent any

    stages {
        stage('Inicio') {
            steps {
                echo 'Empieza la pipeline de Jenkins'
            }
        }

        stage('Ver archivos del repositorio') {
            steps {
                bat 'dir'
            }
        }

        stage('Comprobacion') {
            steps {
                echo 'Repositorio conectado correctamente con GitHub'
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
