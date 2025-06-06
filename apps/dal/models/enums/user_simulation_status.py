class UserSimulationStatus:
    IDLE = 'IDLE'
    PASSED = 'PASSED'
    FAILED = 'FAILED'

    CHOICES = (
        (IDLE, 'In Progress'),
        (PASSED, 'Passed'),
        (FAILED, 'Failed'),
    )
