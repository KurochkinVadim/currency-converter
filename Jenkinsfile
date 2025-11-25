pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }
    
    stages {
        stage('Clean') {
            steps {
                echo 'Cleaning up previous builds...'
                sh 'docker system prune -f || true'
                sh 'docker-compose -f docker-compose.test.yml down || true'
                sh 'docker-compose -f docker-compose.prod.yml down || true'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing application on build machine...'
                sh 'docker-compose -f docker-compose.test.yml up -d --build'
                sh 'sleep 10'
                script {
                    try {
                        sh 'curl -f http://localhost:8002/health'
                        sh 'curl -f http://localhost:8002/api/v1/currencies'
                        sh 'curl -f http://localhost:8002/docs'
                        echo 'All tests passed!'
                    } catch (Exception e) {
                        error 'Tests failed!'
                    } finally {
                        sh 'docker-compose -f docker-compose.test.yml down'
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image on build machine...'
                sh 'docker build -t currency-converter:latest .'
                sh 'docker images | grep currency-converter'
                echo 'Build completed successfully!'
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production environment (second machine simulation)...'
                sh 'docker-compose -f docker-compose.prod.yml down || true'
                sh 'docker-compose -f docker-compose.prod.yml up -d --build'
                sh 'sleep 15'
                script {
                    try {
                        sh 'curl -f http://localhost:8001/health'
                        sh 'curl -f http://localhost:8001/api/v1/currencies'
                        echo 'Production deployment verified!'
                    } catch (Exception e) {
                        error 'Production deployment failed!'
                    }
                }
                echo 'Deployment completed successfully!'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed'
            sh '''
                echo "=== Production Environment URLs ==="
                echo "API: http://localhost:8001"
                echo "Docs: http://localhost:8001/docs" 
                echo "Prometheus: http://localhost:9091"
                echo "Grafana: http://localhost:3001 (admin/admin123)"
                echo "==================================="
            '''
        }
        success {
            echo 'Pipeline succeeded!'
            sh 'docker ps | grep currency-converter'
        }
        failure {
            echo 'Pipeline failed!'
            sh 'docker-compose -f docker-compose.prod.yml logs || true'
        }
    }
}