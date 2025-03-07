pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'osman3/mlops-ml-project'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests/ --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker --version'
                    bat "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%'
                        bat "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                        bat "docker logout"
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            script {
                try {
                    emailext (
                        subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                        body: "Your pipeline has completed successfully.",
                        to: 'mohammadosman31@gmail.com'
                    )
                } catch (Exception e) {
                    echo "Failed to send email: ${e.getMessage()}"
                }
            }
        }
        failure {
            script {
                try {
                    emailext (
                        subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                        body: "Your pipeline has failed. Please check the Jenkins console for details.",
                        to: 'mohammadosman31@gmail.com'
                    )
                } catch (Exception e) {
                    echo "Failed to send email: ${e.getMessage()}"
                }
            }
        }
    }
}
