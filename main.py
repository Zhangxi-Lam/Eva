import traceback
from Eva import Eva
import constants
import time
from pathlib import Path

from utils import get_custom_logger

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig

from utils.control_utils import p_control

logger = get_custom_logger()


def main():
    logger.info("Starting")
    logger.info("="*50)

    try:
        eva = Eva()
        eva.run()
        eva.disconnect()
    except Exception as e:
        logger.error(f"Program execution failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
