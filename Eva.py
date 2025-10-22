import constants
from EvaArm import EvaArm

from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig
from utils import get_custom_logger

logger = get_custom_logger()


class Eva:
    keyboard: KeyboardTeleop
    left_arm: EvaArm
    right_arm: EvaArm

    def __init__(self, l: constants.ArmParams, r: constants.ArmParams):
        self.keyboard = self.init_keyboard()
        self.left_arm = EvaArm(l)
        self.right_arm = EvaArm(r)

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
            left_positions, right_positions = None, None
            if kb_action:
                # Process keyboard input, update target positions
                for key, _ in kb_action.items():
                    if key == constants.RETURN_KEY:
                        return
                    left_positions = self.left_arm.get_next_position(key)
                    right_positions = self.right_arm.get_next_position(key)
            if left_positions:
                self.left_arm.move_to_positions(left_positions)
            if right_positions:
                self.right_arm.move_to_positions(right_positions)

    def disconnect(self):
        logger.info(f"Eva disconnecting...")
        
        # Move back to the default position before disconnect
        self.left_arm.move_to_default_positions()
        self.right_arm.move_to_default_positions()

        # Disconnect
        self.keyboard.disconnect()
        self.left_arm.disconnect()
        self.right_arm.disconnect()
