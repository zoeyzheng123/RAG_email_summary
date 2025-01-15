import logging
import os
import re

import sentry_sdk
from sentry_sdk.integrations.beam import BeamIntegration

logger = logging.getLogger(__name__)

SENTRY_APPLICATION = "RAG_emails"

"""
This is a sentry setup file, but i haven't set it up since it's only dev, not in production 
"""
def initialize_sentry(dsn=None, before_send=None):
    sentry_env = os.environ.get("SENTRY_ENVIRONMENT", "unidentified environment")

    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            release=os.environ.get("SENTRY_RELEASE", "unidentified release"),
            environment=sentry_env,
            integrations=[BeamIntegration()],
            before_send=before_send,
        )
        with sentry_sdk.configure_scope() as scope:
            if workflow_id := os.environ.get("WORKFLOW_NAME"):
                scope.fingerprint = [workflow_id]

            scope.set_tag(
                "workflow_name", os.environ.get("WORKFLOW_NAME", "unidentified")
            )

            scope.set_tag("pod_name", os.environ.get("POD_NAME", "unidentified"))
            scope.set_tag(
                "client", None
            )
            scope.set_tag(
                "SENTRY_ENVIRONMENT",
                "dev",
            )

            logger.info(
                f"Sentry initialized - DSN: {dsn}, ENV: {sentry_env}"
            )

    else:
        logger.warning("SENTRY_DSN not set. Sentry will not be initialized.")


def setup(dsn):
    def ignore_error(hint):
        logger.warning(f"{hint}")
        return re.match(
            ".*HttpError.*'status'\s*:\s*'(5\d{2}|429|408)'",
            str(hint.get("exc_info", "")),
        )  # noqa: W605 (ignore warning about invalid escape sequence)

    def before_send(event, hint):
        if ignore_error(hint):
            return None
        else:
            return event

    initialize_sentry(dsn=dsn, before_send=before_send)


def add_dry_run_tag(dry_run):
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("dry_run", str(dry_run))
