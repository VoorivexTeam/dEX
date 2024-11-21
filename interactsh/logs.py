import re
import time
from utils.file_utils import open_file


def get_oob_server_id(log_file, server_domain):
    """
    Extracts the OOB server ID from the log file.

    :param log_file: The log file to read.
    :param server_domain: The domain of the server (e.g., oast.pro).
    :return: The OOB server ID (correlation ID).
    """
    while True:
        logs = open_file(log_file)
        for log_line in logs:
            match = re.search(rf'(\w+)\.{server_domain}', log_line)
            if match:
                return match.group(1)
        time.sleep(1)  # Wait before checking again


def wait_for_initial_query(log_file, oob_server):
    """
    Waits for the initial query in the log file.

    :param log_file: The log file to read.
    :param oob_server: The OOB server ID.
    :return: Total number of queries and the index of the initial query in the log.
    """
    while True:
        logs = open_file(log_file)
        for index, log_line in enumerate(logs):
            match = re.search(rf'(\d+)\.(\d+)\.[a-z0-9]+\.{oob_server}', log_line)
            if match:
                query_number = match.group(1)
                if query_number == '0':
                    queries_count = int(match.group(2))
                    return queries_count, index
        time.sleep(1)  # Avoid busy-waiting


def collect_data_chunks(log_file, oob_server, chunk_size, queries_count, init_index, timeout):
    """
    Collects data chunks from the logs for a maximum of 10 seconds.

    :param log_file: The log file to read.
    :param oob_server: The OOB server ID.
    :param chunk_size: Size of each chunk.
    :param queries_count: Total number of queries expected.
    :param init_index: Log index where initialization occurred.
    :return: List of received data chunks, up to the time limit.
    """
    receive_logs = [''] * queries_count
    start_time = time.time()
    first_query = False
    
    while True:
        logs = open_file(log_file)
        for index, log_line in enumerate(logs[init_index:], start=init_index):
            match = re.search(rf'(\d+)\.((\d+\.){{{chunk_size},{chunk_size}}})[a-z0-9]+\.{oob_server}', log_line)
            if match:
                data_index = int(match.group(1)) - 1
                data = match.group(2)[:-1]
                if not receive_logs[data_index]:
                    receive_logs[data_index] = data
                    first_query = True
        
        # Check if 10 seconds have passed
        if time.time() - start_time >= timeout and first_query:
            break
        
        # If all data chunks have been received, return early
        if all(receive_logs):
            return receive_logs
        
        time.sleep(1)  # Wait for more logs to arrive

    return receive_logs  # Return whatever is collected in the 10-second window
