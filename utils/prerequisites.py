import shutil
import sys
import logging

def check_prerequisites(binaries):
    """Check if required binary files or commands exist in the system."""
    for binary in binaries:
        if shutil.which(binary) is None:
            logging.error(f"Required binary '{binary}' is not found in the system.")
            sys.exit(1)
    logging.debug("All required binaries are present.")
