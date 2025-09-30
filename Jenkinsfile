pipeline {
    agent any

    environment {
        BOT_TOKEN = credentials('BOT_TOKEN')
    }

    stages {
        // Этап 1: Клонирование репозитория
        stage('Checkout') {
            steps {
                echo 'Cloning the repository...'
                checkout scm
            }
        }

        // Этап 2: Сборка Docker-образа
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building the Docker image...'
                    def imageName = 'tg_calendar_bot:latest'
                    sh "docker build -t ${imageName} ."
                }
            }
        }

        // Этап 3: Запуск/перезапуск бота
        stage('Deploy Bot') {
            steps {
                script {
                    echo 'Deploying the new bot container...'
                    def containerName = 'tg_calendar_bot'
                    def imageName = 'tg_calendar_bot:latest'

                    // Останавливаем и удаляем старую версию бота
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"

                    sh "docker run -d --name ${containerName} -e BOT_TOKEN=${env.telegram_calendar_token} ${imageName}"

                    echo "Bot ${containerName} has been started with the new version."
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            cleanWs()
        }
    }
}
