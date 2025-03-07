pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE_NAME = 'dotyahya/mlops-ml-project'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHONPATH = "${WORKSPACE}"
        PYTHONUNBUFFERED = "1"
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
                    error("Not on master branch. Stopping deployment.")
                }
            }
        }
    }

        stage('Clean Python Environment') {
            steps {
                bat '''
                    set -e
                    python3 -m pip cache purge || true
                    python3 -m pip uninstall -y scikit-learn numpy scipy joblib || true
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        bat '''
                            set -e
                            python3 -m pip install --upgrade pip
                            python3 -m pip install --no-cache-dir -r requirements.txt
                        '''
                    } catch (Exception e) {
                        echo "First attempt failed, retrying..."
                        bat 'python3 -m pip install --no-cache-dir --ignore-installed -r requirements.txt'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat '''
                        set -e
                        docker build -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .
                        docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG $DOCKER_IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        bat '''
                            set -e
                            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                            docker push $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG
                            docker push $DOCKER_IMAGE_NAME:latest
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
                 body: "Pipeline failed! Check Jenkins logs for details."
        }
    }
}
