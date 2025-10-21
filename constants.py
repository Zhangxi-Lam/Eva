from dataclasses import dataclass
from enum import Enum
CALIBRATION_DIR = "./calibration"

# Robot servo
SHOULDER_PAN = "shoulder_pan.pos"
SHOULDER_LIFT = "shoulder_lift.pos"
ELBOW_FLEX = "elbow_flex.pos"
WRIST_FLEX = "wrist_flex.pos"
WRIST_ROLL = "wrist_roll.pos"
GRIPPER = "gripper.pos"

RETURN_KEY = 'm'


class ProgramStatus(Enum):
    IDLE = 'idle'
    IN_PROGRESS = 'in_progress'
    EXIT = 'exit'


@dataclass(frozen=True)
class ArmParams:
    id: str
    port: str
    joint_controls: dict
    default_position: dict
    max_speed = 10
    error = 5


LEFT_ARM_PARAMS = ArmParams(
    id="left_arm",
    port="/dev/tty.usbmodem5AB01583061",
    joint_controls={
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
    },
    default_position={
        SHOULDER_PAN: 67,
        SHOULDER_LIFT: -32,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 0,
        WRIST_ROLL: 0,
        GRIPPER: 0,
    }
)

RIGHT_ARM_PARAMS = ArmParams(
    id="right_arm",
    port="/dev/tty.usbmodem5AB01584211",
    joint_controls={
        'a': (SHOULDER_PAN, 1),
        'z': (SHOULDER_PAN, -1),
        's': (SHOULDER_LIFT, 1),
        'x': (SHOULDER_LIFT, -1),
        'd': (ELBOW_FLEX, 1),
        'c': (ELBOW_FLEX, -1),
        'f': (WRIST_FLEX, 1),
        'v': (WRIST_FLEX, -1),
        'g': (WRIST_ROLL, 1),
        'b': (WRIST_ROLL, -1),
        'h': (GRIPPER, 1),
        'n': (GRIPPER, -1),
    },
    default_position={
        SHOULDER_PAN: 67,
        SHOULDER_LIFT: -32,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 0,
        WRIST_ROLL: 0,
        GRIPPER: 0,
    }
)
