import traceback
import constants
from Eva import Eva

from utils import get_custom_logger

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig

logger = get_custom_logger()


def main():
    logger.info("Starting")
    logger.info("="*50)

    try:
        eva = Eva(constants.LEFT_ARM_CONFIG, constants.RIGHT_ARM_CONFIG)
        eva.run()
        eva.disconnect()
    except Exception as e:
        logger.error(f"Program execution failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
