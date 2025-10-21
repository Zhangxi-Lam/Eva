
LEFT_ARM_ID = "left_arm"
RIGHT_ARM_ID = "right_arm"
LEFT_ARM_PORT = "/dev/tty.usbmodem5AB01583061"
RIGHT_ARM_PORT = "/dev/tty.usbmodem5AB01584211"

CALIBRATION_DIR = "./calibration"

# Robot servo
SHOULDER_PAN = "shoulder_pan.pos"
SHOULDER_LIFT = "shoulder_lift.pos"
ELBOW_FLEX = "elbow_flex.pos"
WRIST_FLEX = "wrist_flex.pos"
WRIST_ROLL = "wrist_roll.pos"
GRIPPER = "gripper.pos"

# Key mapping
IDLE = "idle"
IN_PROGRRESS = 'in_progress'
EXIT = 'exit'

RETURN_KEY = 'x'
JOINT_CONTROLS = {
    '1': (SHOULDER_PAN, 1),
    'q': (SHOULDER_PAN, -1),
    '2': (SHOULDER_LIFT, 1),
    'w': (SHOULDER_LIFT, -1),
    '3': (ELBOW_FLEX, 1),
    'e': (ELBOW_FLEX, -1),
    '4': (WRIST_FLEX, 1),
    'r': (WRIST_FLEX, -1),
    '5': (WRIST_ROLL, 1),
    't': (WRIST_ROLL, -1),
    '6': (GRIPPER, 1),
    'y': (GRIPPER, -1),
}


from enum import Enum
class ProgramStatus(Enum):
    IDLE = 'idle'
    IN_PROGRESS = 'in_progress'
    EXIT = 'exit'
