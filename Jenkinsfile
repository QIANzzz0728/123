pipeline {
    agent { label 'regular-memory-node-c7' }
    
    options {
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '50'))
        disableConcurrentBuilds()
    }
    
    environment {
        PYTHON_VERSION = '3.9'
        IMAGE_NAME = 'streamlit-sales-dashboard'
        DOCKER_REGISTRY = 'your-registry.com' // Replace with your registry
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.BUILD_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                    currentBuild.description = "Branch: ${env.BRANCH_NAME}<br/>Commit: ${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r test_requirements.txt
                '''
            }
        }
        
        stage('Code Quality Checks') {
            parallel {
                stage('Lint with flake8') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            flake8 --max-line-length=88 --extend-ignore=E203,W503 app.py tests/
                        '''
                    }
                }
                
                stage('Format check with black') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            black --check --diff app.py tests/
                        '''
                    }
                }
                
                stage('Type check with mypy') {
                    steps {
                        sh '''
                            source venv/bin/activate
                            mypy app.py --ignore-missing-imports
                        '''
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ -v --cov=app --cov-report=xml --cov-report=html --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    // Publish test results
                    publishTestResults testResultsPattern: 'test-results.xml'
                    
                    // Publish coverage reports
                    publishCoverage adapters: [
                        coberturaAdapter('coverage.xml')
                    ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh '''
                    source venv/bin/activate
                    pip install safety bandit
                    safety check -r requirements.txt
                    bandit -r app.py -f json -o bandit-report.json || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'PR-*'
                }
            }
            steps {
                script {
                    env.IMAGE_TAG = "${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_TAG}"
                    env.IMAGE_TAG_LATEST = "${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:latest"
                }
                sh '''
                    docker build -t ${IMAGE_TAG} .
                    docker tag ${IMAGE_TAG} ${IMAGE_TAG_LATEST}
                '''
            }
        }
        
        stage('Test Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'PR-*'
                }
            }
            steps {
                sh '''
                    # Test that the container starts and responds
                    docker run -d --name test-container -p 8501:8501 ${IMAGE_TAG}
                    sleep 10
                    
                    # Basic health check
                    curl -f http://localhost:8501/_stcore/health || exit 1
                    
                    # Cleanup
                    docker stop test-container
                    docker rm test-container
                '''
            }
        }
        
        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-registry-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_TAG}
                        docker push ${IMAGE_TAG_LATEST}
                    '''
                }
            }
        }
        
        stage('Deploy to Development') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Add your deployment logic here
                    echo "Deploying ${env.IMAGE_TAG} to development environment"
                    // Example: kubectl set image deployment/streamlit-app app=${IMAGE_TAG}
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
            
            // Clean up Docker images
            sh '''
                docker system prune -f
                docker rmi ${IMAGE_TAG} ${IMAGE_TAG_LATEST} || true
            '''
        }
        
        success {
            echo "Pipeline completed successfully!"
            // Add notifications here if needed
        }
        
        failure {
            echo "Pipeline failed!"
            // Add failure notifications here
        }
        
        unstable {
            echo "Pipeline is unstable!"
            // Add unstable notifications here
        }
    }
} 