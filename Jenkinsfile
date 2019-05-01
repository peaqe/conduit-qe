pipeline {
    agent {
        label 'rhsm'
    }
    stages {
        stage('Setup conduit') {
            steps {
                echo 'test'
                dir('conduit') {
                    git 'https://github.com/RedHatInsights/rhsm-conduit.git'
                }
            }
        }
        stage('Clean') {
            steps {
                dir('conduit') {
                    sh './gradlew --no-daemon clean'
                }
            }
        }
        stage('Build') {
            steps {
                dir('conduit') {
                    sh './gradlew --no-daemon assemble'
                }
            }
        }
        stage('Unit tests') {
            steps {
                dir('conduit') {
                    sh './gradlew --no-daemon test'
                }
            }
        }
        stage('Checkstyle') {
            steps {
                dir('conduit') {
                    sh './gradlew --no-daemon checkstyleMain checkstyleTest'
                }
            }
        }
        stage('Setup QE Tests') {
            steps {
                echo 'test'
                dir('conduit-qe') {
                    git 'https://github.com/peaqe/conduit-qe'
                    sh 'sudo dnf install -y pipenv'
                    sh 'pipenv install'
                    // sh 'pipenv run py.test -v conduitqe/tests/api/'
                }
            }
        }
    }
}
