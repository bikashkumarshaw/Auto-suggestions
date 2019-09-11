import argparse

def _define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--es-url", help="specify the database name", type=str, required=True)
    parser.add_argument("--es-port", help="specify the username of the db", type=str, required=True)
    parser.add_argument("--port", help="specify the port to run server", type=int, required=True)
    parser.add_argument("--es-index", help="specify the password of postgresql user", type=str, required=True)
    parser.add_argument("--ip", help="specify the ip of the machine where this service will be hosted", type=str, required=True)
    parser.add_argument("--f-name", help="file containing words to be loaded", type=str, required=True)
    args = parser.parse_args()
    return args
