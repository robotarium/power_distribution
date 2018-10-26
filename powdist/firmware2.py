import vizier.node as node
import RPi.GPIO as GPIO
import time
import argparse
import queue
import netifaces
import json
import log


pins = [14, 15, 16, 18, 20, 21, 24, 25]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def get_mac():
    """Gets the MAC address for the robot from the network config info.

    Returns:
        str: A MAC address for the robot.

    Example:
        >>> print(get_mac())
        AA:BB:CC:DD:EE:FF

    """

    interface = [x for x in netifaces.interfaces() if 'wlan' in x][0]
    return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']


def create_node_descriptor(end_point):
    """Returns a node descriptor for the robot based on the end_point.

    The server_alive link is for the robot to check the MQTT connection periodically.

    Args:
        end_point (str): The ID of the robot.

    Returns:
        dict: A node descriptor of the vizier format for the robot.

    Example:
        >>> node_descriptor(1)

    """
    node_descriptor = \
        {
            'end_point': 'pd_'+end_point,
            'links':
            {
                '/status': {'type': 'DATA'},
            },
            'requests':
            [
                {
                    'link': 'vizier/'+end_point,
                    'type': 'STREAM',
                    'required': False
                },
            ]
        }

    return node_descriptor


def main():

    logger = log.get_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("mac_list", help="JSON file containing MAC to id mapping")
    parser.add_argument("-port", type=int, help="MQTT Port", default=8080)
    parser.add_argument("-host", help="MQTT Host IP", default="localhost")

    # Retrieve the MAC address for the robot
    mac_address = get_mac()

    # Parser and set CLI arguments
    args = parser.parse_args()

    # Retrieve the MAC list file, containing a mapping from MAC address to robot ID
    try:
        f = open(args.mac_list, 'r')
        mac_list = json.load(f)
    except Exception as e:
        print(repr(e))
        print('Could not open file ({})'.format(args.node_descriptor))

    if(mac_address in mac_list):
        robot_id = mac_list[mac_address]
    else:
        print('MAC address {} not in supplied MAC list file'.format(mac_address))
        raise ValueError()

    node_descriptor = create_node_descriptor(robot_id)

    started = False
    pd_node = None
    while (not started):
        pd_node = node.Node(args.host, args.port, node_descriptor)
        try:
            pd_node.start()
            started = True
        except Exception as e:
            logger.critical('Could not start robot node.')
            logger.critical(repr(e))
            pd_node.stop()

        # Don't try to make nodes too quickly
        time.sleep(1)

    status_link = list(pd_node.puttable_links)[0]
    input_link = list(pd_node.subscribable_links)[0]

    status_data = {}

    input_q = pd_node.subscribe(input_link)

    # Initially set GPIO pins high
    for x in pins:
        logger.info('Setting pin {0} as output'.format(x))
        GPIO.setup(x, GPIO.OUT)

    for x in pins:
            logger.info('Setting pin {0} high'.format(x))
            GPIO.output(x, GPIO.HIGH)

    while True:

        print(input_q.qsize())
        msg = input_q.get()

        # Clear out other messages
        while True:
            try:
                msg = input_q.get_nowait()
            except queue.Empty:
                break

        # msg now contains latest msg
        try:
            msg = json.loads(msg.decode(encoding='UTF-8'))
        except Exception as e:
            logger.warning(repr(e))
            continue

        status_data = msg
        pd_node.put(status_link, json.dumps(status_data))

        # At this point, msg contains a valid JSON message
        # structure is {'pins': 0/1}
        if('state' in msg):
            state = msg['state']
            if(state is 1):
                logger.info('Setting GPIO high')
                for x in pins:
                    GPIO.output(x, GPIO.HIGH)
            else:
                logger.info('Setting GPIO low')
                for x in pins:
                    GPIO.output(x, GPIO.LOW)


if __name__ == "__main__":
    main()
