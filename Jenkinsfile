pipeline {
    agent any

    parameters {
        string(name: 'NEW_IP', defaultValue: '', description: 'IP de la nouvelle EC2')
        password(name: 'AWS_ACCESS_KEY_ID', description: 'AWS Access Key')
        password(name: 'AWS_SECRET_ACCESS_KEY', description: 'AWS Secret Key')
        string(name: 'AWS_REGION', defaultValue: 'eu-west-3', description: 'AWS Region')
        string(name: 'SETUP_SCRIPT_PATH', defaultValue: '/home/florian-andr/Documents/setup.sh', description: 'Chemin absolu du script setup.sh à copier sur EC2')
        string(name: 'PEM_KEY_PATH', defaultValue: '/home/florian-andr/.ssh/ipsa.pem', description: 'Chemin absolu de la clé PEM à utiliser pour la connexion SSH')
    }

    stages {
        stage('Copier setup.sh et exécuter') {
            steps {
                script {
                    echo "Copie du script setup.sh depuis ${params.SETUP_SCRIPT_PATH} vers l'instance EC2"

                    // Écriture du script de commandes distantes dans un fichier temporaire
                    writeFile file: 'remote_commands.sh', text: '''
                        chmod +x /home/ubuntu/setup.sh
                        /home/ubuntu/setup.sh
                    '''.stripIndent()

                    sh """
                        sudo -u florian-andr ls -l ${params.SETUP_SCRIPT_PATH}
                        sudo -u florian-andr scp -i ${params.PEM_KEY_PATH} ${params.SETUP_SCRIPT_PATH} ubuntu@${params.NEW_IP}:/home/ubuntu/
                        sudo -u florian-andr scp -i ${params.PEM_KEY_PATH} remote_commands.sh ubuntu@${params.NEW_IP}:/home/ubuntu/
                        sudo -u florian-andr ssh -i ${params.PEM_KEY_PATH} ubuntu@${params.NEW_IP} 'bash /home/ubuntu/remote_commands.sh'
                    """
                }
            }
        }

        stage('Créer le fichier .env') {
            steps {
                script {
                    def envContent = """
                        AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        AWS_REGION=${AWS_REGION}
                    """.stripIndent()

                    writeFile file: 'env_content.txt', text: envContent

                    sh """
                        sudo -u florian-andr scp -i ${params.PEM_KEY_PATH} env_content.txt ubuntu@${params.NEW_IP}:/home/ubuntu/.env
                        sudo -u florian-andr ssh -i ${params.PEM_KEY_PATH} ubuntu@${params.NEW_IP} '
                            mv /home/ubuntu/.env /home/ubuntu/projets_groupe/Projet_federateur_IA/.env &&
                            chmod 600 /home/ubuntu/projets_groupe/Projet_federateur_IA/.env
                        '
                    """
                }
            }
        }
    }
}
