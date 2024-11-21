import subprocess
import logging


def start_client(server, log_file='interactsh.logs', poll_interval=5):
    """
    Starts the interactsh client with the specified server and poll interval.
    
    :param poll_interval: Interval in seconds for polling the server.
    :param server: The interactsh server to use.
    :param log_file: File where logs are written.
    :return: subprocess.Popen object for the running process.
    """
    logging.info('Starting interactsh client...')
    process = subprocess.Popen(
        f'interactsh-client -poll-interval {poll_interval} -server {server}',
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT,
        shell=True
    )
    return process
