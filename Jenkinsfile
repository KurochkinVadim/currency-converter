pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
        COMPOSE_PROJECT_NAME = "jenkins-${BUILD_ID}"
    }
    
    stages {
        stage('Clean') {
            steps {
                echo 'Cleaning up previous builds...'
                sh '''
                    docker system prune -f || true
                    docker-compose -f docker-compose.test.yml down || true
                    docker-compose -f docker-compose.prod.yml down || true
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing application...'
                sh '''
                    # Запускаем тестовые контейнеры
                    docker-compose -f docker-compose.test.yml up -d --build
                    sleep 15
                    
                    # Получаем ID тестового контейнера
                    CONTAINER_ID=$(docker-compose -f docker-compose.test.yml ps -q web)
                    
                    # Тестируем внутри контейнера
                    docker exec $CONTAINER_ID curl -f http://localhost:8000/health
                    docker exec $CONTAINER_ID curl -f http://localhost:8000/api/v1/currencies
                    
                    echo "All tests passed!"
                '''
            }
            post {
                always {
                    sh 'docker-compose -f docker-compose.test.yml down || true'
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t currency-converter:latest .'
                sh 'docker images | grep currency-converter'
                echo 'Build completed successfully!'
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production environment...'
                sh '''
                    docker-compose -f docker-compose.prod.yml down || true
                    docker-compose -f docker-compose.prod.yml up -d --build
                    sleep 20
                    
                    # Проверяем продакшен (порт 8001 доступен с хоста)
                    curl -f http://localhost:8001/health
                    curl -f http://localhost:8001/api/v1/currencies
                    
                    echo "Production deployment verified!"
                '''
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