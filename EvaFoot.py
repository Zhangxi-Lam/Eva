from EvaRobot import EvaRobot
import constants

from utils.LogFormatter import get_custom_logger

logger = get_custom_logger()


class EvaFoot(EvaRobot):

    def __init__(self, config: constants.EvaRobotConfig):
        super().__init__(config)
        self.bus.connect()


if __name__ == "__main__":
    foot = EvaFoot(constants.FOOT_CONFIG)
    pos = foot.get_current_position()
