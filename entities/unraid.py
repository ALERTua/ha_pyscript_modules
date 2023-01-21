from imports import *
import paramiko


class Unraid:
    def __init__(self):
        self.ssh_host = constants.UNRAID_SSH_HOST
        self.ssh_port = constants.UNRAID_SSH_PORT
        self.ssh_username = constants.UNRAID_SSH_USERNAME
        self.ssh_password = constants.UNRAID_SSH_PASSWORD
        self.ssh_key_path = constants.UNRAID_SSH_KEY_PATH
#         log.debug(f"""{self.__class__.__name__}
# host: {self.ssh_host}
# port: {self.ssh_port}
# username: {self.ssh_username}
# password: {'*' * len(self.ssh_password) if self.ssh_password else 'None'}
# ssh_key_path: {self.ssh_key_path}
# """)

    def ssh_cmd_ha(self, command):
        data = {
            'host': self.ssh_host,
            'port': self.ssh_port,
            'user': self.ssh_username,
            'pass': self.ssh_password,
            'command': command
        }
        return ssh_command.exec_command(data=data)

    def ssh_cmd(self, command, sudo=False):
        if sudo:
            command = f"sudo -S -p '' {command}"

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
        client.connect(
            hostname=self.ssh_host,
            port=self.ssh_port,
            username=self.ssh_username,
            password=self.ssh_password,
            pkey=key,
        )
        log.debug(f"Executing {self.__class__.__name__} SSH command: {command}")
        _stdin, _stdout, _stderr = client.exec_command(command)
        retval = None
        if _stdout:
            retval = _stdout.channel.recv_exit_status()
            _stdout = _stdout.read().decode()
        if _stderr:
            _stderr = _stderr.read().decode()
        # log.debug(_stdout.read().decode())
        client.close()
        return retval, _stdout, _stderr

    def reset_ups(self):
        retval, _stdout, _stderr = self.ssh_cmd('bash /boot/config/_scripts/ups_reset.sh')
        log.debug(f"{self.__class__.__name__} UPS Reset result {retval}\n{_stdout}\n{_stderr}")
        return retval, _stdout, _stderr
