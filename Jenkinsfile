pipeline {
	agent any
	stages {
		stage('Checkout SCM') {
			steps {
				git 'https://github.com/Karissa-Chua-Hanyi/webapp.git'
			}
		}
		stage('Build') {
            steps {
                // Build your project using Maven
                sh 'mvn clean install'
				sh '/var/jenkins_home/apache-maven-3.6.3/bin/mvn --batch-mode -V -U -e clean verify -Dsurefire.useFile=false -Dmaven.test.failure.ignore'
            }
        }
		stage('Integration Test') {
            steps {
                // Run your integration tests using JUnit
                sh 'mvn test'
            }
        }
		stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
				// Run OWASP Dependency Check
                sh 'mvn dependency-check:check'
			}
		}
		stage('UI Testing') {
            steps {
                // Assuming you have Selenium tests
                // Start your application or deploy it to a test environment

                // Run Selenium tests
                sh 'mvn verify -Pui-tests'
            }
        }
		stage ('Analysis') {
            steps {
                sh '/var/jenkins_home/apache-maven-3.6.3/bin/mvn --batch-mode -V -U -e checkstyle:checkstyle pmd:pmd pmd:cpd findbugs:findbugs'
            }
        }
		stage('Code Quality Check via SonarQube') {
			steps {
				script {
					def scannerHome = tool 'SonarQube';
						withSonarQubeEnv('SonarQube') {
						sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=OWASP -Dsonar.sources=."
						}
				}
			}
		}
		stage('Deploy') {
            steps {
                // Assuming you have a deployment step, deploy your application
                // For example, deploy to a test environment
                sh 'mvn deploy'
            }
        }
	}	
	post {
		always {
            junit testResults: '**/target/surefire-reports/TEST-*.xml'
            recordIssues enabledForFailure: true, tools: [mavenConsole(), java(), javaDoc()]
            recordIssues enabledForFailure: true, tool: checkStyle()
            recordIssues enabledForFailure: true, tool: spotBugs(pattern:
            '**/target/findbugsXml.xml')
            recordIssues enabledForFailure: true, tool: cpd(pattern: '**/target/cpd.xml')
            recordIssues enabledForFailure: true, tool: pmdParser(pattern: '**/target/pmd.xml')
			recordIssues enabledForFailure: true, tool: sonarQube()
        }
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
	}
	
}