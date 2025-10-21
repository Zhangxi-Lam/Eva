import constants

from lerobot.robots.so100_follower import SO100Follower
from lerobot.teleoperators.keyboard import KeyboardTeleop


def p_control(lrobot: SO100Follower, rrobot: SO100Follower, keyboard: KeyboardTeleop, momentum): 
    positions = lrobot.get_observation()
    kb_action = keyboard.get_action()
    if kb_action:
        # Process keyboard input, update target positions
        for key, _ in kb_action.items():
            if key == constants.RETURN_KEY:
                return constants.ProgramStatus.EXIT, None, positions 
            if key in constants.JOINT_CONTROLS:
                joint_name, delta = constants.JOINT_CONTROLS[key]
                positions[joint_name] += delta * momentum
        return constants.ProgramStatus.IN_PROGRESS, kb_action, positions
    else:
        return constants.ProgramStatus.IDLE, None, positions
