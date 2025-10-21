import traceback
import constants
import time
from pathlib import Path

from utils import get_custom_logger

from lerobot.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.teleoperators.keyboard import KeyboardTeleop, KeyboardTeleopConfig

logger = get_custom_logger()


def get_current_position(robot: SO100Follower):
    # Get current robot state
    current_obs = robot.get_observation()

    # Extract current joint positions
    current_positions = {}
    for key, value in current_obs.items():
        if key.endswith('.pos'):
            motor_name = key.removesuffix('.pos')
            current_positions[motor_name] = value

    return current_positions


def move_to_zero_position(robot: SO100Follower, duration=3.0, kp=0.5):
    """
    Uses P control to slowly move robot to zero position

    Args:
        robot: Robot instance
        duration: Time required to move to zero position (seconds)
        kp: Proportional gain
    """
    # Zero position targets
    zero_positions = {
        'shoulder_pan': 0.0,
        'shoulder_lift': 0.0,
        'elbow_flex': 0.0,
        'wrist_flex': 0.0,
        'wrist_roll': 0.0,
        'gripper': 0.0
    }

    # Calculate control steps
    control_freq = 50  # 50 Hz control frequency
    total_steps = int(duration * control_freq)
    step_time = 1.0 / control_freq

    logger.info(
        f"Will move to zero position in {duration} seconds using P control, control frequency: {control_freq}Hz, proportional gain: {kp}")

    for step in range(total_steps):
        current_positions = get_current_position(robot)

        robot_action = {}
        for joint_name, target_pos in zero_positions.items():
            if joint_name in current_positions:
                current_pos = current_positions[joint_name]
                error = target_pos - current_pos
                # P control: output = kp * error
                control_output = kp * error

                new_position = current_pos + control_output
                robot_action[f"{joint_name}.pos"] = new_position

        if robot_action:
            robot.send_action(robot_action)

        # Display progress
        if step % (control_freq // 2) == 0:  # Display progress every 0.5 seconds
            progress = (step / total_steps) * 100
            print(f"Moving to zero position progress: {progress:.1f}%")
            print(current_positions)
            print(robot_action)

        time.sleep(step_time)

    logger.info("Robot has moved to zero position")


def main():
    logger.info("Starting")
    logger.info("="*50)

    try:
        lp = constants.LEFT_ARM_PORT
        rp = constants.RIGHT_ARM_PORT
        logger.info(f"Connecting to port: {lp}, {rp}")

        # Configure robot
        lconfig = SO100FollowerConfig(
            port=lp, id=constants.LEFT_ARM_ID, calibration_dir=Path(constants.CALIBRATION_DIR))
        rconfig = SO100FollowerConfig(
            port=rp, id=constants.RIGHT_ARM_ID, calibration_dir=Path(constants.CALIBRATION_DIR))
        lrobot = SO100Follower(lconfig)
        rrobot = SO100Follower(rconfig)

        # Configure keyboard
        keyboard_config = KeyboardTeleopConfig()
        keyboard = KeyboardTeleop(keyboard_config)

        # Connect devices
        lrobot.connect()
        rrobot.connect()
        keyboard.connect()
        logger.info("Devices connected successfully!")

        # Read starting joint angles
        logger.info("Reading starting joint angles...")
        current_positions = get_current_position(lrobot)
        print(current_positions)

        move_to_zero_position(lrobot, duration=3.0)
        move_to_zero_position(rrobot, duration=3.0)

        # Initialize target positions to current positions (integers)
        # target_positions = {
        #     'shoulder_pan': 0.0,
        #     'shoulder_lift': 0.0,
        #     'elbow_flex': 0.0,
        #     'wrist_flex': 0.0,
        #     'wrist_roll': 0.0,
        #     'gripper': 0.0
        # }
        # while True:
        #     try:
        #         kb_action = keyboard.get_action()
        #         if kb_action:
        #             for key, value in keyboard_action.items():
        #                 if key == 'x':
        #                     return

        #                 # Joint control mapping
        #                 joint_controls = {
        #                     'q': ('shoulder_pan', -1),    # Joint1 decrease
        #                     'a': ('shoulder_pan', 1),     # Joint1 increase
        #                     'w': ('shoulder_lift', -1),   # Joint2 decrease
        #                     's': ('shoulder_lift', 1),    # Joint2 increase
        #                     'e': ('elbow_flex', -1),      # Joint3 decrease
        #                     'd': ('elbow_flex', 1),       # Joint3 increase
        #                     'r': ('wrist_flex', -1),      # Joint4 decrease
        #                     'f': ('wrist_flex', 1),       # Joint4 increase
        #                     't': ('wrist_roll', -1),      # Joint5 decrease
        #                     'g': ('wrist_roll', 1),       # Joint5 increase
        #                     'y': ('gripper', -1),         # Joint6 decrease
        #                     'h': ('gripper', 1),          # Joint6 increase
        #                 }

        #                 if key in joint_controls:
        #                     joint_name, delta = joint_controls[key]
        #                     if joint_name in target_positions:
        #                         current_target = target_positions[joint_name]
        #                         new_target = int(current_target + delta)
        #                         target_positions[joint_name] = new_target
        #                         print(
        #                             f"Updated target position {joint_name}: {current_target} -> {new_target}")

        #     except Exception as e:
        #         pass

        logger.info("Program ended")
    except Exception as e:
        logger.error(f"Program execution failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
