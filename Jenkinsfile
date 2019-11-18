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
                dir('conduit-qe') {
                    git 'https://github.com/peaqe/conduit-qe'
                    sh 'sudo dnf install -y pipenv'
                    sh 'pipenv install'
                    configFileProvider(
                        [configFile(fileId: '17df57b9-d207-4d7a-bff2-9111558642e4', targetLocation: 'conduitqe.conf', variable: 'CONDUITQE_CONFIG')]) {
                        echo "Copying configuration $CONDUITQE_CONFIG"
                    }
                    sh 'pipenv run pytest -v -m "not openshift" conduitqe/tests/api/'
                }
            }
        }
        stage('Setup QE Tests on CI') {
            steps {
                sh 'pwd'
                dir('conduit-qe') {
                    sh 'sudo dnf install -y origin-clients'
                    sh 'sudo dnf install -y pipenv python36'
                    sh 'pipenv run pytest -v -m openshift conduitqe/tests/api/'
                }
            }
        }
        stage('Setup QE Multiple Accounts Tests on CI') {
            steps {
                sh 'pwd'
                dir('conduit-qe') {
                    configFileProvider(
                        [configFile(fileId: '5635e91a-d428-4a35-93a1-b20c5e744f94', targetLocation: 'conduitqe.conf', variable: 'CONDUITQE_CONFIG')]) {
                        echo "Copying configuration $CONDUITQE_CONFIG"
                    }
                    configFileProvider(
                        [configFile(fileId: 'fafec977-5232-4825-9ff5-2df4e62bdca9', targetLocation: 'accounts.txt', variable: 'ACCOUNTS_LIST')]) {
                        echo "Copying accounts list $ACCOUNTS_LIST"
                    }
                    sh 'while IFS= read -r line; do pipenv run env $line pytest -v -m openshift conduitqe/tests/api/ ; done < accounts.txt'
                }
            }
        }
    }
}
