import subprocess
import time
import socket
import resource


class Server:
    """
    This class is intended to be run from a pytest fixture.

    It is specifically meant to be used to start and stop a MQTT server program.
    """
    def __init__(self, program_path, port=1883, timeout=5, nofiles=None):
        """
        Initialize the instance.
        """
        self.program_path = program_path
        self.popen = None
        self.port = port
        self.timeout = timeout
        self.nofiles = nofiles

        self.outs = None
        self.errs = None

    def start(self):
        """
        Start the program under test.
        """
        # Make sure there is nothing listening on the port before the program is started.
        socket_v4 = None
        try:
            socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            socket_v4.connect(('localhost', self.port))
            raise Exception(f"there is something listening on {self.port} and it is not us")
        except ConnectionRefusedError:
            pass
        finally:
            if socket_v4:
                socket_v4.close()

        # This should be inherited to the program under test.
        nofiles = self.nofiles
        if nofiles:
            print(f"setting nofiles limit to {nofiles}")
            resource.setrlimit(resource.RLIMIT_NOFILE, (nofiles, nofiles))

        # TODO: is this going to hang the program once the pipe is filled ?
        #       i.e. should there be a thread that does read the stdout/stderr ala communicate() ?
        self.popen = subprocess.Popen([self.program_path, "-p", f"{self.port}"])

        #
        # Wait for the port to accept connections (optional - can be turned off by setting timeout=0).
        #
        # Two related notes:
        #   - firstly, this does not guarantee that the open port belongs to the program under test.
        #   - secondly, the connection established can intermingle with some test performed, e.g.
        #     file descriptor usage wise etc.
        #
        if self.timeout > 0:
            start_time = time.monotonic()
            socket_v4 = None
            i = 0
            while True:
                if time.monotonic() - start_time > self.timeout:
                    print(f"Connect timeout ({self.timeout}s) expired")
                    break
                try:
                    socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                    socket_v4.connect(('localhost', self.port))
                    print("Connected successfully - server seems to be running")
                    break
                except ConnectionRefusedError:
                    print(f"Still no IPv4 connect to {self.port}, sleeping for a bit (iteration #{i})")
                    i += 1
                    time.sleep(0.1)
                    pass
                finally:
                    if socket_v4:
                        socket_v4.close()

    def stop(self):
        """
        Check if the test program is still running. If yes, terminate it.
        """
        print(f"Server object cleanup (port {self.port})")
        if self.popen:
            popen = self.popen
            #
            # Firstly check if the process is gone before attempting to terminate it so that the return code
            # can be retrieved. This is handy in case the program has crashed during the test.
            #
            if popen.poll():
                # Here, it is no longer possible to get stdout/stderr of the program using popen.communicate().
                print(f"The program exited with {popen.returncode}")
            else:
                print("Terminating the program")
                popen.terminate()
                self.outs, self.errs = popen.communicate(timeout=10)
                popen.kill()
