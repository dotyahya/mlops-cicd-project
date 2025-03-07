pipeline {
    agent any
    
    triggers {
        githubPush()  // This will trigger Jenkins on push events
    }
    
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'osman3/mlops-ml-project'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHONPATH = "${WORKSPACE}"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Check PR Merge') {
            steps {
                script {
                    def branch = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
                    echo "Current branch: ${branch}"
                    
                    if (branch != 'master') {
                        error("Not on master branch. Stopping deployment.")
                    }

                    // Ensure the build was triggered by a PR merge event
                    def isPRMerged = currentBuild.getBuildCauses('hudson.model.Cause$RemoteCause')
                    if (!isPRMerged) {
                        error("Not triggered by a PR merge. Exiting...")
                    }
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Python Environment') {
            steps {
                sh 'python3 -m pip cache purge'
                sh 'python3 -m pip uninstall -y scikit-learn numpy scipy joblib'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        sh 'python3 -m pip install --upgrade pip'
                        sh 'python3 -m pip install --no-cache-dir -r requirements.txt'
                    } catch (Exception e) {
                        echo "First attempt failed, retrying..."
                        sh 'python3 -m pip install --no-cache-dir --ignore-installed -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/test.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                    sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh 'docker logout'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            mail to: 'mohammadosman31@gmail.com',
                 subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                 body: "PR Merged. Pipeline completed successfully!"
        }
        failure {
            mail to: 'mohammadosman31@gmail.com',
                 subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                 body: "PR merge detected, but pipeline failed! Check logs."
        }
    }
}
