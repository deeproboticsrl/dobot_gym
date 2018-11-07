import click
from dobot_gym.utils.dobot_controller import DobotController
from glob import glob

# import ipdb
available_ports = glob('/dev/tty*USB*')
if len(available_ports) == 0:
    print('no port found for Dobot Magician')
    exit(1)
def_port = available_ports[0]


def print_help():
    print("Dobot CLI Controller")
    print("Enter m <x> <y> <z>  to move to position x,y,z with rotation r(add later) ")
    print("Enter g <e> <t> to set gripper to position e(0/1) and enable control for t seconds")
    print("Enter j <cmd> <isJoint> <isqueued>")
    print("Enter q to exit")
    print("Enter h to print this msg")


@click.command()
@click.option('--port', type=str, default=def_port, help='Port Name')
def main(port):
    dobot = DobotController(port=def_port)
    print_help()
    # ipdb.set_trace()
    while True:
        try:
            inp = input("Dobot>").split()
            cmd = inp[0]

            if cmd == 'q':
                break
            elif cmd == 'h':
                print_help()

            elif cmd == 'g':
                e = int(inp[1])
                t = float(inp[2])
                dobot.grip(e, t)

            elif cmd == 'm': ## add r later
                x, y, z= [int(x) for x in inp[1:]]
                dobot.movexyz(x, y, z)
            elif cmd == 'j':
                com, isJoint, q = [int(x) for x in inp[1:]]
                print("com received")
                dobot.jog(cmd=com, isJoint=isJoint, q=q)
            else:
                dobot.disconnect()
                exit()
        except Exception as e :
            print("Invalid Command or Value. Exiting.")
            print(e)
            exit()


if __name__ == '__main__':
    main()
