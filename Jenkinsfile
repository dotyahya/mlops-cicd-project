pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'osman3/mlops-ml-project'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHONPATH = "${WORKSPACE}"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Check PR Target Branch') {
            steps {
                script {
                    if (env.CHANGE_TARGET != 'master') {
                        error("This pipeline only runs for pull requests targeting the master branch.")
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean Python Environment') {
            steps {
                bat 'python -m pip cache purge'
                bat 'python -m pip uninstall -y scikit-learn numpy scipy joblib'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        bat 'python -m pip install --upgrade pip --user'
                        bat 'python -m pip install --no-cache-dir -r requirements.txt --user'
                    } catch (Exception e) {
                        echo "First attempt failed, trying alternative installation..."
                        bat 'python -m pip install --no-cache-dir --ignore-installed -r requirements.txt --user'
                    }
                }
            }
        }

        stage('Verify Installation') {
            steps {
                bat 'python -c "import sklearn; import numpy; import scipy; import joblib; print(\'All packages imported successfully\')"'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests/test.py -v --junitxml=test-results.xml'
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
                        body: "The pull request from `test` to `master` has been successfully merged and deployed.",
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
                        body: "The deployment failed. Check Jenkins logs for details.",
                        to: 'mohammadosman31@gmail.com'
                    )
                } catch (Exception e) {
                    echo "Failed to send email: ${e.getMessage()}"
                }
            }
        }
    }
}
