pipeline {
    // 1. Agent Declaration: Run on any available agent
    agent any

    // 2. Tools Section: Use the Python installation we configured
    tools {
        python 'python3' // This name must match the one in Manage Jenkins > Tools
    }

    // 3. Stages of the Pipeline
    stages {
        // STAGE 1: Checkout code from GitHub
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                // 'credentialsId' must match the ID you created in Jenkins
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/Script-eng/alx-backend-python.git'
            }
        }

        // STAGE 2: Install dependencies
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        // STAGE 3: Run Tests and Generate Report
        stage('Run Tests') {
            steps {
                echo 'Running tests with pytest...'
                // Generate a JUnit XML report for Jenkins to parse
                sh 'pytest --junitxml=test-report.xml'
            }
        }
    }

    // 4. Post-build Actions: Always run regardless of stage success or failure
    post {
        always {
            echo 'Archiving test results...'
            // Use the junit plugin to publish the generated test report
            junit 'test-report.xml'
        }
    }
}
