from instruction_graph.components.Memory import BaseMemory
from enum import Enum


class PepperMemory(BaseMemory):
    def __init__(self, session):
        super(BaseMemory, self).__init__()
        self.session = session
        self.state = States.SEARCHING

        # self.memProxy = self.session.service("ALMemory")
        self.faceProxy = self.session.service("ALFaceDetection")
        self.face = "Test_Face"
        self.faceProxy.subscribe(self.face, 500, 0.0)

    def cleanup(self):
        self.faceProxy.unsubscribe(self.face)

    def memory_name(self):
        return "Pepper_Example_Memory"


class States(Enum):
    SEARCHING = 0
    FOUND_PERSON = 1
