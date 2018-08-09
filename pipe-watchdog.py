#!/usr/bin/env python
import logging
import os
import select
import sys


TIMEOUT_SECONDS = 60 * 4
BUFFER_SIZE_BYTES = 1<<12


logger = logging.getLogger("pipe-watchdog")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
    )

    while True:
        # this call to `select` will block (for up to TIMEOUT_SECONDS) until the file descriptor(s) specified have data
        # ready to be acted upon - here we're only giving it file descriptor 0 (stdin) to monitor for readability
        ready_for_read, _, _ = select.select((0,), (), (), TIMEOUT_SECONDS)

        if not ready_for_read:
            # select must have timed out
            logger.error(f"Did not receive input for {TIMEOUT_SECONDS}s. Aborting.")
            # an arbitrary exit code, but at least collisions should be unlikely making it unambiguous
            sys.exit(131)
            # previous processes in pipeline should receive SIGPIPE, hopefully aborting too.

        # now that we know this shouldn't block we'll try and read as many bytes as we immediately can (up to
        # BUFFER_SIZE_BYTES) from file descriptor 0 (stdin)
        buf = os.read(0, BUFFER_SIZE_BYTES)
        if not buf:
            logger.info(f"Reached EOF. Exiting normally.")
            sys.exit(0)

        # forward our buffer of bytes back out to file descriptor 1 (stdout)
        os.write(1, buf)
