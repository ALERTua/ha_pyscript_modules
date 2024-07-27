from imports import *
import paramiko


class Unraid:
    def __init__(self, host=UNRAID_SSH_HOST):
        self.ssh_host = host or UNRAID_SSH_HOST
        self.ssh_port = UNRAID_SSH_PORT
        self.ssh_username = UNRAID_SSH_USERNAME
        self.ssh_password = UNRAID_SSH_PASSWORD
        self.ssh_key_path = UNRAID_SSH_KEY_PATH
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


class VM:
    def __init__(self, name, unraid: Unraid = None):
        self.name = name
        self.unraid = unraid or Unraid()
    
    def turn_on(self):
        self.unraid.ssh_cmd(f'virsh start "{self.name}"')

    def turn_off(self):
        self.unraid.ssh_cmd(f'virsh shutdown "{self.name}"')

    def suspend(self):
        self.unraid.ssh_cmd(f'virsh dompmsuspend "{self.name}"')

    def resume(self):
        self.unraid.ssh_cmd(f'virsh dompmwakeup "{self.name}"')
