import constants
import time

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig

from utils.LogFormatter import get_custom_logger

logger = get_custom_logger()

class EvaArm:
    params: constants.ArmParams
    robot: SO100Follower

    def __init__(self, params: constants.ArmParams):
        self.params = params
        port, id, calibration_dir = params.port, params.id, params.calibration_dir
        logger.info(f"Initializing arm using {port}, {id}, {calibration_dir}")

        config = SO100FollowerConfig(
            port=port, id=id, calibration_dir=calibration_dir)
        self.robot = SO100Follower(config)
        self.robot.connect()
    
    def calibrate(self):
        return self.robot.calibrate()

    def get_observation(self):
        return self.robot.get_observation()
    
    def disconnect(self):
        return self.robot.disconnect()
    
    def get_next_position(self, key:str):
        if key in self.params.joint_controls:
            positions = self.robot.get_observation()
            joint_name, delta = self.params.joint_controls[key]
            positions[joint_name] += delta * self.params.speed
            return positions
        return None
            
    def reach_position(self, target_positions, positions):
        if not target_positions:
            return False

        for key, value in target_positions.items():
            delta = value - positions[key]
            if abs(delta) > self.params.error:
                return False
        return True

    def move_to_default_position(self):
        return self.move_to_position(self.params.default_position)
    
    def move_to_position(self, target_positions):
        logger.info(f"Moving to position {target_positions} ")

        last_position = None
        while True:
            positions = self.robot.get_observation()
            # Check if robot has reached target_positions
            if self.reach_position(target_positions, positions):
                logger.info(f"Moving to position {target_positions} done!")
                return 

            # Get new positions
            for joint_name, target_pos in target_positions.items():
                delta = target_pos - positions[joint_name]
                delta = self.params.max_speed if delta > self.params.max_speed else delta
                delta = -self.params.max_speed if delta < -self.params.max_speed else delta
                positions[joint_name] += delta

            # Check if the new positions is roughly the same as the last positions
            if self.reach_position(last_position, positions):
                current_positions = self.robot.get_observation()
                logger.warning(f"Moving to position {target_positions} stuck at {current_positions}!")
                return

            # Move to new positions and wait
            self.robot.send_action(positions)
            last_position = positions
            time.sleep(self.params.control_interval)

