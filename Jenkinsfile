pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your_username/python_project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the Python script...'
                // Add your deployment logic here, e.g., upload to a server or schedule a job.
            }
        }
    }
}
