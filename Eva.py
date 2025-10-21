import time
import logging
from pathlib import Path
import constants

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig
from utils import get_custom_logger

logger = get_custom_logger()

class Eva:
    keyboard: KeyboardTeleop
    left_arm: SO100Follower
    right_arm: SO100Follower

    def __init__(self, momentum=1, control_freq=50) -> None:
        self.keyboard = self.init_keyboard()
        self.left_arm = self.init_arm(constants.LEFT_ARM_PORT, constants.LEFT_ARM_ID, constants.CALIBRATION_DIR)
        self.right_arm = self.init_arm(constants.RIGHT_ARM_PORT, constants.RIGHT_ARM_ID, constants.CALIBRATION_DIR)
        self.control_freq = control_freq
        self.momentum = momentum

        logger.info(f"Eva initialization complete!")
    
    def init_keyboard(self) -> KeyboardTeleop:
        config = KeyboardTeleopConfig()
        keyboard = KeyboardTeleop(config)
        keyboard.connect()
        return keyboard
    
    def init_arm(self, port:str, id:str, calibration_dir_path: str) -> SO100Follower:
        logger.info(f"Initializing arm using {port}, {id}, {calibration_dir_path}")
        config =  SO100FollowerConfig(
            port=port, id=id, calibration_dir=Path(calibration_dir_path))
        arm = SO100Follower(config)
        arm.connect()
        return arm 

    def p_control(self):
        positions = self.left_arm.get_observation()
        kb_action = self.keyboard.get_action()
        if kb_action:
            # Process keyboard input, update target positions
            for key, _ in kb_action.items():
                if key == constants.RETURN_KEY:
                    return constants.ProgramStatus.EXIT, None, positions 
                if key in constants.JOINT_CONTROLS:
                    joint_name, delta = constants.JOINT_CONTROLS[key]
                    positions[joint_name] += delta * self.momentum
            return constants.ProgramStatus.IN_PROGRESS, kb_action, positions
        else:
            return constants.ProgramStatus.IDLE, None, positions


    def run(self):
        logger.info(f"Eva running, momentum {self.momentum} control frequency {self.control_freq}")

        interval = 1.0 / self.control_freq
        last_kb_action = None
        while True:
            try:
                status, kb_action, positions = self.p_control()
                if status == constants.ProgramStatus.EXIT:
                    logger.info(f"Exiting, final positions {positions}")
                    return
                if kb_action:
                    self.left_arm.send_action(positions)
                if kb_action == last_kb_action:
                    self.momentum += 1
                else:
                    self.momentum = 1
                    last_kb_action = kb_action
                time.sleep(interval)
            except Exception as e:
                pass


    def disconnect(self):
        logger.info(f"Eva disconnecting...")
        self.keyboard.disconnect()
        self.left_arm.disconnect()
        self.right_arm.disconnect()