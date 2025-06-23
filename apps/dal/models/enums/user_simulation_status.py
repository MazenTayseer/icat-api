class UserSimulationStatus:
    IDLE = 'IDLE'
    PASSED_OR_IGNORED = 'PASSED_OR_IGNORED'
    FAILED = 'FAILED'

    CHOICES = (
        (IDLE, 'In Progress'),
        (PASSED_OR_IGNORED, 'Passed or Ignored'),
        (FAILED, 'Failed'),
    )
