# coding=utf-8
# --------------------------------------------------------------------------------
# Project: HydraXcel
# Author: Carel van Niekerk, Benjamin Ruppik
# Year: 2025
# Group: Dialogue Systems and Machine Learning Group
# Institution: Heinrich Heine University Düsseldorf
# --------------------------------------------------------------------------------
#
# This code was generated with the help of AI writing assistants
# including GitHub Copilot, ChatGPT, Bing Chat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Set up exception logging."""

import logging
import os
import sys
import warnings

logger = logging.getLogger("__main__")

__all__ = ["setup_exception_logging"]


def setup_exception_logging(
    logger: logging.Logger = logger,
) -> None:
    """Set up a custom exception handler that logs uncaught exceptions.

    Args:
    ----
        logger: An instance of a logger to be used for logging exceptions.

    Side effects:
        - Sets the HYDRA_FULL_ERROR environment variable to "1".
        - Sets the sys.excepthook to a custom exception handler that logs exceptions.

    """
    # Setting this environment variable to "1" makes Hydra print the full stack trace.
    print("Setting HYDRA_FULL_ERROR environment variable to '1'.")
    os.environ["HYDRA_FULL_ERROR"] = "1"
    print(f"{os.environ['HYDRA_FULL_ERROR'] = }")

    def handle_exception(
        exc_type,  # noqa: ANN001
        exc_value,  # noqa: ANN001
        exc_traceback,  # noqa: ANN001
    ) -> None:
        """Handle uncaught exceptions by logging them, except for KeyboardInterrupt.

        This function is designed to be compatible with sys.excepthook.
        Thus, you should not call this function directly, but rather set
        it as the sys.excepthook. Also make sure you do not change the signature of
        this function, as it is called by sys.excepthook.

        Args:
        ----
            exc_type:
                The exception type.
            exc_value:
                The exception value.
            exc_traceback:
                The traceback object.

        """
        if issubclass(
            exc_type,
            KeyboardInterrupt,
        ):
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback,
            )
            return

        logger.critical(
            "Uncaught exception",
            exc_info=(
                exc_type,
                exc_value,
                exc_traceback,
            ),
        )

    def handle_warning(  # noqa: PLR0913
        message,  # noqa: ANN001
        category,  # noqa: ANN001
        filename,  # noqa: ANN001
        lineno,  # noqa: ANN001
        file=None,  # noqa: ANN001, ARG001
        line=None,  # noqa: ANN001, ARG001
    ) -> None:
        """Handle warnings by logging them."""
        logger.warning(f"{category.__name__} at {filename}:{lineno}: {message}")  # noqa: G004

    sys.excepthook = handle_exception
    warnings.showwarning = handle_warning  # type: ignore[assignment]
