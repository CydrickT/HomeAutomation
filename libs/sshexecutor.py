import paramiko

class SshExecutor():

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.connect(self.hostname, username=self.username, password=self.password)

    def execute(self, command):
        self.client.exec_command(command)

    def close(self):
        self.client.close()

