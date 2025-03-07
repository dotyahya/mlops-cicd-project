pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE_NAME = 'dotyahya/mlops-ml-project'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Check Branch') {
            steps {
                script {
                    def branch = env.GIT_BRANCH ?: 'unknown'
                    echo "Current branch: ${branch}"

                    if (branch != 'origin/master' && branch != 'master') {
                        currentBuild.result = 'ABORTED'
                        error('Not on master branch. Stopping deployment.')
                    }
                }
            }
        }

        stage('Clean Python Environment') {
            steps {
                bat '''
                    pip cache purge || true
                    pip uninstall -y scikit-learn numpy scipy joblib || true
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        bat '''
                            pip install --upgrade pip
                            pip install --no-cache-dir -r requirements.txt
                        '''
                    } catch (Exception e) {
                        echo 'First attempt failed, retrying...'
                        bat 'pip install --no-cache-dir --ignore-installed -r requirements.txt'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat '''
                        echo "DOCKER_IMAGE_NAME: ${env.DOCKER_IMAGE_NAME}"
                        echo "DOCKER_IMAGE_TAG: ${env.DOCKER_IMAGE_TAG}"
                        docker build -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} .
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        bat '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin
                            docker push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}
                            docker logout
                        '''
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
            mail to: 'dev.yahyu@gmail.com',
                 subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                 body: "Pipeline completed successfully! Docker image pushed to DockerHub as ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} and ${DOCKER_IMAGE_NAME}:latest"
        }
        failure {
            mail to: 'dev.yahyu@gmail.com',
                 subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                 body: 'Pipeline failed! Check Jenkins logs for details.'
        }
    }
}
