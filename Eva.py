import time
from pathlib import Path
import constants

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig
from utils import get_custom_logger

logger = get_custom_logger()


class Eva:
    keyboard: KeyboardTeleop
    left_arm_params: constants.ArmParams
    right_arm_params: constants.ArmParams
    left_arm: SO100Follower
    right_arm: SO100Follower

    def __init__(self, l: constants.ArmParams, r: constants.ArmParams, calibration_dir: str, speed=10, control_freq=50) -> None:
        self.keyboard = self.init_keyboard()
        self.left_arm_params = l
        self.right_arm_params = r
        self.left_arm = self.init_arm(l, calibration_dir)
        self.right_arm = self.init_arm(r, calibration_dir)

        self.speed = speed
        self.control_interval = 1.0 / control_freq

        logger.info(f"Eva initialization complete!")

    def init_keyboard(self) -> KeyboardTeleop:
        config = KeyboardTeleopConfig()
        keyboard = KeyboardTeleop(config)
        keyboard.connect()
        return keyboard

    def init_arm(self, params, calibration_dir) -> SO100Follower:
        port, id = params.port, params.id
        logger.info(f"Initializing arm using {port}, {id}, {calibration_dir}")

        config = SO100FollowerConfig(
            port=port, id=id, calibration_dir=Path(calibration_dir))
        arm = SO100Follower(config)
        arm.connect()
        return arm

    def move_to_position(self, robot: SO100Follower, target_position, max_speed, error):
        logger.info(f"Moving to position {target_position}, {max_speed}")
        while True:
            positions = robot.get_observation()
            done = True
            for joint_name, target_pos in target_position.items():
                if joint_name in positions:
                    delta = target_pos - positions[joint_name]
                    if abs(delta) < error:
                        continue
                    done = False
                    delta = max_speed if delta > max_speed else delta
                    delta = -max_speed if delta < -max_speed else delta
                    positions[joint_name] += delta
            if done:
                logger.info(f"Moving to position {target_position} done!")
                return
            robot.send_action(positions)
            time.sleep(self.control_interval)

    def get_next_position(self, speed):
        left_positions = self.left_arm.get_observation()
        right_positions = self.right_arm.get_observation()
        kb_action = self.keyboard.get_action()
        if kb_action:
            # Process keyboard input, update target positions
            for key, _ in kb_action.items():
                if key == constants.RETURN_KEY:
                    return False, None, None
                if key in self.left_arm_params.joint_controls:
                    joint_name, delta = self.left_arm_params.joint_controls[key]
                    left_positions[joint_name] += delta * speed
                if key in self.right_arm_params.joint_controls:
                    joint_name, delta = self.right_arm_params.joint_controls[key]
                    right_positions[joint_name] += delta * speed

            return True, left_positions, right_positions
        else:
            return False, left_positions, right_positions

    def run(self):
        logger.info(
            f"Eva running, speed {self.speed} interval {self.control_interval}")

        while True:
            has_action, left_positions, right_positions = self.get_next_position(self.speed)
            if not left_positions:
                self.move_to_position(self.left_arm, self.left_arm_params.default_position,
                                      self.left_arm_params.max_speed, self.left_arm_params.error)
                self.move_to_position(self.right_arm, self.right_arm_params.default_position,
                                      self.right_arm_params.max_speed, self.right_arm_params.error)
                return
            if has_action:
                self.move_to_position(self.left_arm, left_positions,
                                      self.left_arm_params.max_speed, self.left_arm_params.error)
                self.move_to_position(self.right_arm, right_positions,
                                      self.right_arm_params.max_speed, self.right_arm_params.error)

    def disconnect(self):
        logger.info(f"Eva disconnecting...")
        self.keyboard.disconnect()
        self.left_arm.disconnect()
        self.right_arm.disconnect()
