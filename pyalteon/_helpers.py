# -*- coding: utf-8 -*-
"""Define helper functions used by classes in this module."""

from functools import wraps
import logging

from ._compat import unquote


def traffic_log(traffic_logger=None, method="GET"):
    """Log traffic for the wrapped function.

    This will wrap any function with a call to `logger.debug()` displaying useful before and after information from
    API calls.  This obeys the log level set in logging, so if the level is not set to "DEBUG", no messages will be
    logged.

    Note: The "DEBUG" level should *never* be used in production.

    :param obj traffic_logger: a logging.Logger to use for logging messages.
    :param str method: The HTTP method being used, to be noted in the logging. (Default: "GET")
    """
    # pylint: disable=too-many-branches
    def decorator(func):
        """Wrap the actual decorator so a reference to the function can be returned."""
        @wraps(func)
        # pylint: disable=too-many-branches
        def log_traffic(*args, **kwargs):
            """Decorate the wrapped function."""
            # Make sure traffic_logger was set correctly
            if not isinstance(traffic_logger, logging.Logger):
                raise Exception("traffic_log: No logging.Logger instance provided")

            # Check if the URL or headers exist in the parameters
            # Note: *self* will be the first argument, so actual arguments start after that.
            url = kwargs.get("url", "")
            if not url:
                if len(args) > 1:
                    url = args[1]
            headers = kwargs.get("headers", "")
            if not headers:
                if len(args) > 2:
                    headers = args[2]
            data = kwargs.get("data", "")
            if not data:
                if len(args) > 3:
                    data = args[3]

            # Print out before messages with URL and header data
            if url:
                traffic_logger.debug(f"Performing a {method} on url: {url}")
            if headers:
                traffic_logger.debug(f"Extra request headers: {headers}")
            if data:
                traffic_logger.debug(f"Data: {data}")

            # Run the wrapped function
            try:
                result = func(*args, **kwargs)
            except HttpError as herr:
                # If it's of type HttpError, we can still usually get the result data
                traffic_logger.debug(f"Result code: {herr.http_result.status_code}")
                traffic_logger.debug(f"Result headers: {herr.http_result.headers}")
                traffic_logger.debug(f"Text result: {herr.http_result.text}")

                # Re-raise the original exception
                raise herr
            except Exception as exc:
                # Re-raise the original exception
                raise exc

            # If everything went fine, more logging
            if result:
                traffic_logger.debug(f"Result code: {result.status_code}")
                traffic_logger.debug(f"Result headers: {result.headers}")
                traffic_logger.debug(f"Text result: {result.text}")
            return result
        return log_traffic
    return decorator


class HttpError(Exception):
    """Serve as a generic Exception indicating an HTTP error."""

    def __init__(self, result):
        """Initialize the exception class."""
        data = None

        # Store the result in the exception object
        self.__result = result

        # Generic last-resort error message
        msg = "Unknown HTTP error"

        # Make sure that not receiving JSON doesn't trigger a nested Exception
        try:
            data = result.json()
        except Exception:  # pylint: disable=broad-except
            data = {}

        if "description" in data:
            msg = unquote(data["description"])

        message = f"{self.__result.status_code}s: {msg}"

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

    @property
    def http_result(self):
        """Return the internal __result variable.

        :return obj: A requests.Response object
        """
        return self.__result
