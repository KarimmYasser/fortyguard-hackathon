class FortyGuardError(Exception):
    """Any error returned by the FortyGuard API."""


class TaskFailedError(FortyGuardError):
    """The async task finished with status=failed."""


class TaskTimeoutError(FortyGuardError):
    """The async task did not finish within the polling budget."""


class ActivityNotReadyError(FortyGuardError):
    """The status endpoint 404'd — the activity isn't queryable yet.

    This is expected for a short window right after submission (eventual
    consistency); pollers should retry rather than fail.
    """

    def __init__(self, activity_id: str) -> None:
        self.activity_id = activity_id
        super().__init__(
            f"Activity {activity_id} is not visible yet (status endpoint returned 404)."
        )
