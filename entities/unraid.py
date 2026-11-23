from imports import *


@pyscript_executor
def _ssh_run(host, port, username, password, key_path, command):
    # paramiko blocks: the key file, the TCP connect and the wait for the command run in a thread
    import paramiko

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path) if key_path else None
        client.connect(
            hostname=host,
            port=int(port or 22),
            username=username,
            password=password,
            pkey=key,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10,
        )
        _stdin, stdout, stderr = client.exec_command(command, timeout=300)
        retval = stdout.channel.recv_exit_status()
        return retval, stdout.read().decode(), stderr.read().decode()
    finally:
        client.close()


@pyscript_executor
def _tailscale_ssh_run(host, username, command):
    # Tailscale SSH checks the tailnet identity of the HA node, so the client offers no key ("none" auth)
    import socket
    import paramiko

    sock = socket.create_connection((host, 22), timeout=10)
    transport = paramiko.Transport(sock)
    try:
        transport.start_client(timeout=10)
        transport.auth_none(username)
        chan = transport.open_session(timeout=10)
        chan.settimeout(300)
        chan.exec_command(command)
        stdout = chan.makefile('r').read().decode()
        stderr = chan.makefile_stderr('r').read().decode()
        return chan.recv_exit_status(), stdout, stderr
    finally:
        transport.close()


class Unraid:
    def __init__(
        self,
        host=UNRAID_SSH_HOST,
        port=UNRAID_SSH_PORT,
        username=UNRAID_SSH_USERNAME,
        password=UNRAID_SSH_PASSWORD,
        ssh_key_path=UNRAID_SSH_KEY_PATH,
        tailscale_host=UNRAID_TAILSCALE_HOST,
    ):
        self.ssh_host = host or UNRAID_SSH_HOST
        self.ssh_port = port or UNRAID_SSH_PORT
        self.ssh_username = username or UNRAID_SSH_USERNAME
        self.ssh_password = password or UNRAID_SSH_PASSWORD
        self.ssh_key_path = ssh_key_path or UNRAID_SSH_KEY_PATH
        # None or '' turns Tailscale SSH off and leaves only the key
        self.tailscale_host = tailscale_host

    #         log.debug(f"""{self.__class__.__name__}
    # host: {self.ssh_host}
    # port: {self.ssh_port}
    # username: {self.ssh_username}
    # password: {'*' * len(self.ssh_password) if self.ssh_password else 'None'}
    # ssh_key_path: {self.ssh_key_path}
    # """)

    def ssh_cmd_ha(self, command):
        host = (self.ssh_host,)
        port = self.ssh_port
        user = self.ssh_username
        password = self.ssh_password
        command = command
        kw = {}
        if password:
            kw['pass'] = password
        return ssh_command.exec_command(
            host=host, port=port, user=user, command=command, **kw
        )

    def ssh_cmd(self, command, sudo=False, debug=False):
        if sudo:
            command = f"sudo -S -p '' {command}"

        log.debug(f"Executing {self.__class__.__name__} SSH command: {command}")
        result = None
        if self.tailscale_host:
            try:
                result = _tailscale_ssh_run(self.tailscale_host, self.ssh_username, command)
            except Exception as e:
                # the key over the LAN is the fallback when Tailscale SSH is down or refuses the node
                log.warning(
                    f"{self.__class__.__name__}: Tailscale SSH to {self.tailscale_host} failed: "
                    f"{type(e).__name__}: {e}. Trying the key over the LAN."
                )
        if result is None:
            result = _ssh_run(
                self.ssh_host,
                self.ssh_port,
                self.ssh_username,
                self.ssh_password,
                self.ssh_key_path,
                command,
            )
        retval, _stdout, _stderr = result

        if debug:
            log.debug(f"stdout: {_stdout}\nstderr: {_stderr}\nretval: {retval}")

        return retval, _stdout, _stderr

    def reset_ups(self):
        retval, _stdout, _stderr = self.ssh_cmd(
            'bash /boot/config/_scripts/ups_reset.sh'
        )
        log.debug(
            f"{self.__class__.__name__} UPS Reset result {retval}\n{_stdout}\n{_stderr}"
        )
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
