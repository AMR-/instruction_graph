import argparse
import qi


# controller -- pass the class which takes as first __init__ parameter a naoqi session
# *args -- any additional args for the controller class constructor
# returns the instantiated controller with the naoqi connection
def init_qi_controller(controller, *c_args):
    p_args = get_pepper_parser().parse_args()
    if p_args.ip is None or p_args.port is None:
        raise ValueError("Please specify ip and port.")
    try:
        qi_app = initialize_qi_app(p_args)
        print("Connected to Naoqi successfully at ip \"" + p_args.ip + "\" on port " + str(p_args.port) + ".\n")
        return controller(qi_app, c_args) if c_args else controller(qi_app)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + p_args.ip + "\" on port " + str(p_args.port) + ".\n")
        return controller(None, c_args) if c_args else controller(None)


def get_pepper_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, help="Naoqi port number")
    return parser


def initialize_qi_app(args):
    # Initialize qi framework.
    connection_url = "tcp://" + args.ip + ":" + str(args.port)
    print(connection_url)
    qi_app = qi.Application(["StandInit", "--qi-url=" + connection_url])
    return qi_app
