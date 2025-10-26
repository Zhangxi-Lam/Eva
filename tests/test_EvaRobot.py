import pytest
from constants import EvaRobotConfig, RobotPosition, SHOULDER_PAN
from EvaRobot import EvaRobot
from lerobot.motors.feetech import FeetechMotorsBus


class FakeFeetechMotorsBus(FeetechMotorsBus):

    def __init__(self):
        pass

    def sync_read(self, data_name: str):
        return {
            "shoulder_pan": 1,
            "shoulder_lift": 2,
            "elbow_flex": 3,
            "wrist_flex": 4,
            "wrist_roll": 5,
            "gripper": 6,
        }


@pytest.fixture
def fake_config():
    return EvaRobotConfig(id="test",
                          port="/dev/tty.usbmodem5AB01584211",
                          motors={},
                          robot_controls={
                              'q': (SHOULDER_PAN, 1),
                          },
                          default_position={})


def test_get_current_position(fake_config):
    bus = FakeFeetechMotorsBus()
    robot = EvaRobot(fake_config, bus)
    assert robot.get_current_position() == RobotPosition({
        "shoulder_pan.pos": 1,
        "shoulder_lift.pos": 2,
        "elbow_flex.pos": 3,
        "wrist_flex.pos": 4,
        "wrist_roll.pos": 5,
        "gripper.pos": 6,
    })


def test_get_next_position(fake_config):
    bus = FakeFeetechMotorsBus()
    robot = EvaRobot(fake_config, bus)
    assert robot.get_next_position("q") == RobotPosition({
        "shoulder_pan.pos": 11,
        "shoulder_lift.pos": 2,
        "elbow_flex.pos": 3,
        "wrist_flex.pos": 4,
        "wrist_roll.pos": 5,
        "gripper.pos": 6,
    })


def test_reach_position(fake_config):
    bus = FakeFeetechMotorsBus()
    robot = EvaRobot(fake_config, bus)
    assert robot.reach_position(
        RobotPosition({
            "shoulder_pan.pos": 11,
            "shoulder_lift.pos": 2,
            "elbow_flex.pos": 3,
            "wrist_flex.pos": 4,
            "wrist_roll.pos": 5,
            "gripper.pos": 6,
        }),
        RobotPosition({
            "shoulder_pan.pos": 11,
            "shoulder_lift.pos": 4,
            "elbow_flex.pos": 5,
            "wrist_flex.pos": 2,
            "wrist_roll.pos": 3,
            "gripper.pos": 2,
        })) == True
