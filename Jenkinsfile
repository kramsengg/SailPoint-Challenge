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
          . .venv/bin/activate && 
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
            //   python3 -m unittest discover -s tests/unit       
          sh """
            pytest
          """
        }
      }
    }

    stage('Build image for deployment') { 
      agent any
      steps {
        script {
          sh 'docker build -t amarchandran/sp-challenge:latest .'
          sh 'docker build -t amarchandran/sp-challenge-flask:1.0.0-draft -f Dockerfile.flask .'
        }
      }
    }


    stage('Push image for deployment') { 
      agent any
      steps {
        script {
          sh 'docker push amarchandran/sp-challenge:latest '
          sh 'docker push amarchandran/sp-challenge-flask:1.0.0-latest'
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