from constants import EvaRobotConfig, RETURN_KEY
from EvaArm import EvaArm
from EvaFoot import EvaFoot

from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig
from utils import get_custom_logger

logger = get_custom_logger()


class Eva:
    keyboard: KeyboardTeleop
    left_arm: EvaArm
    right_arm: EvaArm

    def __init__(self, left_arm_config: EvaRobotConfig, right_arm_config: EvaRobotConfig,
                 foot_config: EvaRobotConfig):
        self.keyboard = self.init_keyboard()
        self.left_arm = EvaArm(left_arm_config)
        self.right_arm = EvaArm(right_arm_config)
        self.foot = EvaFoot(foot_config)

        logger.info(f"Eva initialization complete!")

    def init_keyboard(self) -> KeyboardTeleop:
        config = KeyboardTeleopConfig()
        keyboard = KeyboardTeleop(config)
        keyboard.connect()
        return keyboard

    def run(self):
        logger.info(f"Eva running...")

        while True:
            kb_action = self.keyboard.get_action()
            left_position, right_position, foot_position = None, None, None
            if kb_action:
                # Process keyboard input, update target positions
                for key, _ in kb_action.items():
                    if key == RETURN_KEY:
                        return
                    left_position = self.left_arm.get_next_position(key)
                    right_position = self.right_arm.get_next_position(key)
                    foot_position = self.foot.get_next_position(key)
            if left_position:
                self.left_arm.move_to_position_in_loop(left_position)
            if right_position:
                self.right_arm.move_to_position_in_loop(right_position)
            if foot_position:
                self.foot.move_to_position_in_loop(foot_position)

    def disconnect(self):
        logger.info(f"Eva disconnecting...")

        # Move back to the default position before disconnect
        self.left_arm.move_to_default_position()
        self.right_arm.move_to_default_position()

        # Disconnect
        self.keyboard.disconnect()
        self.left_arm.disconnect()
        self.right_arm.disconnect()
