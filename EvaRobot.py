import time
import draccus
from pathlib import Path
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import MotorCalibration
from lerobot.utils.errors import DeviceNotConnectedError

from constants import EvaRobotConfig, RobotPosition
from utils.LogFormatter import get_custom_logger

logger = get_custom_logger()


class EvaRobot:
    config: EvaRobotConfig
    bus: FeetechMotorsBus

    # If bus is provided, use it, otherwise create a new one
    def __init__(self, config: EvaRobotConfig, bus: FeetechMotorsBus = None):
        self.config = config
        if bus is not None:
            self.bus = bus
        else:
            self.bus = FeetechMotorsBus(port=config.port,
                                        motors=config.motors,
                                        calibration=self._load_calibration(
                                            config.calibration_dir))

    @property
    def is_connected(self) -> bool:
        return self.bus.is_connected

    def connect(self):
        return self.bus.connect()

    def disconnect(self):
        return self.bus.disconnect()

    def _load_calibration(self, dir: Path) -> dict[str, MotorCalibration]:
        fpath = dir / f"{self.config.id}.json"
        with open(fpath) as f, draccus.config_type("json"):
            return draccus.load(dict[str, MotorCalibration], f)

    def get_current_position(self) -> RobotPosition:
        pos = self.bus.sync_read("Present_Position")
        pos = {f"{motor}.pos": val for motor, val in pos.items()}
        return RobotPosition(pos)

    # Get robot's next position after the given key
    def get_next_position(self, key: str) -> RobotPosition:
        if key in self.config.robot_controls:
            position = self.get_current_position()
            servo_name, delta = self.config.robot_controls[key]
            position[servo_name] += delta * self.config.speed
            return position
        return None

    # Check whether robot has reached the target position
    def reach_position(self, target: RobotPosition,
                       current: RobotPosition) -> bool:
        if not target:
            return False

        for key, value in target.items():
            delta = value - current[key]
            if abs(delta) > self.config.error:
                return False
        return True

    def move_to_default_position(self):
        return self.move_to_position(self.config.default_position)

    def move_to_position(self, target: RobotPosition):
        if not self.is_connected:
            raise DeviceNotConnectedError(
                f"{self.config.id} is not connected.")

        goal_pos = {
            key.removesuffix(".pos"): val
            for key, val in target.items() if key.endswith(".pos")
        }
        self.bus.sync_write("Goal_Position", goal_pos)

    def move_to_position_in_loop(self, target: RobotPosition):
        logger.info(f"Moving to position {target} ")

        last_position = None
        current = self.get_current_position()
        while True:
            # Check if robot has reached target_positions
            if self.reach_position(target, current):
                logger.info(f"Moving to position {target} done!")
                return

            # Get new positions
            for servo_name, target_pos in target.items():
                delta = target_pos - current[servo_name]
                delta = self.config.speed if delta > self.config.speed else delta
                delta = -self.config.speed if delta < -self.config.speed else delta
                current[servo_name] += delta

            # Check if the new positions is roughly the same as the last positions
            if self.reach_position(last_position, current):
                current = self.get_current_position()
                logger.warning(
                    f"Moving to position {target} stuck at {current}!")
                return

            # Move to new positions and wait
            self.move_to_position(current)
            last_position = current
            time.sleep(self.config.control_interval)
