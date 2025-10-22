from pathlib import Path
from dataclasses import dataclass
from typing import TypedDict

# Robot servo
SHOULDER_PAN = "shoulder_pan.pos"
SHOULDER_LIFT = "shoulder_lift.pos"
ELBOW_FLEX = "elbow_flex.pos"
WRIST_FLEX = "wrist_flex.pos"
WRIST_ROLL = "wrist_roll.pos"
GRIPPER = "gripper.pos"

RETURN_KEY = 'm'


class ArmPositions(dict[str, float]):
    def __str__(self):
        return str("\n" + "\t\n".join(f"{k}: {v:.1f}" for k, v in self.items()) + "\n")



@dataclass(frozen=True)
class ArmParams:
    id: str
    port: str
    joint_controls: dict
    default_positions: ArmPositions
    control_interval = 1.0 / 50
    speed = 10
    max_speed = 10
    error = 5
    calibration_dir = Path("./calibration")


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
    default_positions=ArmPositions({
        SHOULDER_PAN: 67,
        SHOULDER_LIFT: -32,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 0,
        WRIST_ROLL: 0,
        GRIPPER: 0,
    })
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
    default_positions=ArmPositions({
        SHOULDER_PAN: 0,
        SHOULDER_LIFT: -84,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 11,
        WRIST_ROLL: -5,
        GRIPPER: 0,
    })
)
