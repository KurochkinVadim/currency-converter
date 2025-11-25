pipeline {
    agent any
    
    stages {
        stage('Build and Deploy') {
            steps {
                echo 'Building and deploying...'
                sh '''
                    # Останавливаем старые контейнеры
                    docker-compose -f docker-compose.prod.yml down || true
                    
                    # Собираем и запускаем
                    docker-compose -f docker-compose.prod.yml up -d --build
                    
                    # Ждём запуска
                    sleep 30
                    
                    # Проверяем
                    curl -f http://localhost:8001/ || exit 1
                    curl -f http://localhost:8001/health || exit 1
                    
                    echo "Deployment successful!"
                    echo "Production is running on http://localhost:8001"
                '''
            }
        }
    }
}