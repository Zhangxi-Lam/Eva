LEFT_ARM_ID = "left_arm"
RIGHT_ARM_ID = "right_arm"
LEFT_ARM_PORT = "/dev/tty.usbmodem5AB01583061"
RIGHT_ARM_PORT = "/dev/tty.usbmodem5AB01584211"

CALIBRATION_DIR = "./calibration"

# Robot servo
SHOULDER_PAN = "shoulder_pan.pos"

JOINT_CONTROLS = {
    'q': (SHOULDER_PAN, -1),
    'a': (SHOULDER_PAN, 1)
}