pipeline {
  options {
    buildDiscarder(logRotator(numToKeepStr: '10')) // Retain history on the last 10 builds
    timestamps() // Append timestamps to each line
    timeout(time: 20, unit: 'MINUTES') // Set a timeout on the total execution time of the job
  }
  agent any 
  stages {  // Define the individual processes, or stages, of your CI pipeline
    stage('Checkout') { // Checkout (git clone ...) the projects repository
      steps {
        checkout scm
      }
    }
    stage('Setup') { // Install any dependencies you need to perform testing
      steps {
        script {
          sh """
          python3 -m venv .venv && 
          source .venv/bin/activate && 
          pip install -r requirements.txt
          """
        }
      }
    }
    // stage('Linting') { // Run pylint against your code
    //   steps {
    //     script {
    //       sh """
    //       pylint **/*.py
    //       """
    //     }
    //   }
    // }
    stage('Unit Testing') { // Perform unit testing
      steps {
        script {
          sh """
          python3 -m unittest discover -s tests/unit
          """
        }
      }
    }
    
  }  
  post {
    failure {
      script {
        msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"
        
        // slackSend message: msg, channel: env.SLACK_CHANNEL
    }
  }    
}
}