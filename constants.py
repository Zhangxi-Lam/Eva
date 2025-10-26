from pathlib import Path
from dataclasses import dataclass
from lerobot.motors import Motor, MotorNormMode

# Robot servo
SHOULDER_PAN = "shoulder_pan.pos"
SHOULDER_LIFT = "shoulder_lift.pos"
ELBOW_FLEX = "elbow_flex.pos"
WRIST_FLEX = "wrist_flex.pos"
WRIST_ROLL = "wrist_roll.pos"
GRIPPER = "gripper.pos"
LEFT_WHEEL = "left_wheel"
RIGHT_WHEEL = "right_wheel"
MID_WHEEL = "mid_wheel"

RETURN_KEY = 'm'


class RobotPosition(dict[str, float]):
    def __str__(self):
        return str("\n" + "\t\n".join(f"{k}: {v:.1f}" for k, v in self.items()) + "\n")

@dataclass(frozen=True)
class EvaRobotConfig:
    id: str
    port: str
    calibration_dir = Path("./calibration")
    motors: dict[str, Motor]
    robot_controls: dict
    default_position: RobotPosition
    speed = 10
    error = 5
    control_interval = 1.0 / 50



LEFT_ARM_CONFIG = EvaRobotConfig(
    id="left_arm",
    port="/dev/tty.usbmodem5AB01583061",
    motors = {
        "shoulder_pan": Motor(1, "sts3215", MotorNormMode.DEGREES),
        "shoulder_lift": Motor(2, "sts3215", MotorNormMode.DEGREES),
        "elbow_flex": Motor(3, "sts3215", MotorNormMode.DEGREES),
        "wrist_flex": Motor(4, "sts3215", MotorNormMode.DEGREES),
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.DEGREES),
        "gripper": Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
    },
    robot_controls={
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
    default_position=RobotPosition({
        SHOULDER_PAN: 67,
        SHOULDER_LIFT: -32,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 0,
        WRIST_ROLL: 0,
        GRIPPER: 0,
    })
)

RIGHT_ARM_CONFIG = EvaRobotConfig(
    id="right_arm",
    port="/dev/tty.usbmodem5AB01584211",
    motors = {
        "shoulder_pan": Motor(1, "sts3215", MotorNormMode.DEGREES),
        "shoulder_lift": Motor(2, "sts3215", MotorNormMode.DEGREES),
        "elbow_flex": Motor(3, "sts3215", MotorNormMode.DEGREES),
        "wrist_flex": Motor(4, "sts3215", MotorNormMode.DEGREES),
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.DEGREES),
        "gripper": Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
    },
    robot_controls={
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
    default_position=RobotPosition({
        SHOULDER_PAN: 0,
        SHOULDER_LIFT: -84,
        ELBOW_FLEX: 0,
        WRIST_FLEX: 11,
        WRIST_ROLL: -5,
        GRIPPER: 0,
    })
)

FOOT_CONFIG = EvaRobotConfig(
    id="base_foot",
    port="/dev/tty.usbmodem5AB01584211",
    motors={
        LEFT_WHEEL: Motor(7, "sts3215", MotorNormMode.RANGE_M100_100),
        RIGHT_WHEEL: Motor(8, "sts3215", MotorNormMode.RANGE_M100_100),
        MID_WHEEL: Motor(9, "sts3215", MotorNormMode.RANGE_M100_100),
    },
    robot_controls={},
    default_position=None
)