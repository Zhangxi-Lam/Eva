import constants
import time

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig

from utils.LogFormatter import get_custom_logger
from EvaRobot import EvaRobot
from constants import EvaRobotConfig

logger = get_custom_logger()

class EvaArm(EvaRobot):
    def __init__(self, config: EvaRobotConfig):
        super().__init__(config)
        self.bus.connect()
    