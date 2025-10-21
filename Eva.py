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
    left_arm_params: constants.ArmParams
    right_arm_params: constants.ArmParams
    left_arm: SO100Follower
    right_arm: SO100Follower

    def __init__(self, l: constants.ArmParams, r: constants.ArmParams, calibration_dir: str, momentum=1, control_freq=50) -> None:
        self.keyboard = self.init_keyboard()
        self.left_arm_params = l
        self.right_arm_params = r
        self.left_arm = self.init_arm(l, calibration_dir)
        self.right_arm = self.init_arm(r, calibration_dir)
        self.control_interval = 1.0 / control_freq
        self.momentum = momentum

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
        logger.info(
            f"Eva running, momentum {self.momentum} interval {self.control_interval}")

        last_kb_action = None
        while True:
            status, kb_action, positions = self.p_control()
            if status == constants.ProgramStatus.EXIT:
                self.move_to_position(self.left_arm, self.left_arm_params.default_position,
                                      self.left_arm_params.max_speed, self.left_arm_params.error)
                return
            if kb_action:
                self.left_arm.send_action(positions)
            if kb_action == last_kb_action:
                self.momentum += 1
            else:
                self.momentum = 1
                last_kb_action = kb_action
            time.sleep(self.control_interval)

    def disconnect(self):
        logger.info(f"Eva disconnecting...")
        self.keyboard.disconnect()
        self.left_arm.disconnect()
        self.right_arm.disconnect()
