pipeline {
    options { buildDiscarder(logRotator(numToKeepStr: '50')) }
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
        stage('Run') {
            steps {
                dir('conduit') {
                    // Build and run conduit in backgrount (to prevent job from
                    // hanging)
                    sh './gradlew assemble'
                    sh 'java -jar build/libs/rhsm-conduit-*.jar &'
                }
            }
        }
        stage('Setup QE Tests') {
            steps {
                // Setup Conduit-QE Config File
                sh 'pwd'
                configFileProvider([configFile(fileId: '17df57b9-d207-4d7a-bff2-9111558642e4', targetLocation: 'conduitqe.conf')]) {
                    echo 'Copying conduitqe.conf'
                }
                dir('conduit-qe') {
                    git 'https://github.com/peaqe/conduit-qe'
                    sh 'sudo dnf install -y pipenv'
                    sh 'pipenv install'
                    sh 'pipenv run pytest -v -m "not openshift" conduitqe/tests/api/'
                }
            }
        }
        stage('Setup QE Tests on CI') {
            steps {
                // Setup Conduit-QE Config File
                sh 'pwd'
                configFileProvider([configFile(fileId: '17df57b9-d207-4d7a-bff2-9111558642e4', targetLocation: 'conduitqe.conf')]) {
                    echo 'Copying conduitqe.conf'
                }
                dir('conduit-qe') {
                    sh 'sudo dnf install -y origin-clients'
                    sh 'pipenv run pytest --log-cli-level=DEBUG -v -m "openshift" conduitqe/tests/api/'
                }
            }
        }
    }
}
