from instruction_graph import Manager
from PepperMemory import PepperMemory
from PepperPrimitiveLibrary import PepperPrimitiveLibrary, PrimitiveIds as Pid
import math


class Controller(object):
    def __init__(self, qi_app):
        self.qi = qi_app
        self.qi.start()
        self.ig_file_name = "generated/pepper_demo.ig"
        self.memory_object = PepperMemory(self.qi.session)
        self.library = PepperPrimitiveLibrary()
        self.igm = Manager(library=self.library, memory=self.memory_object)

    def build_instruction_graph(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action(Pid.SAY, args=["I am Pepper.  I am going to search for a human by rotating."])

        self.igm.ig.add_loop(Pid.IS_SEARCHING)
        self.igm.ig.add_action(Pid.ROTATE, args=['L', 0.5*math.pi])

        self.igm.ig.add_if(Pid.IS_HUMAN_VISIBLE)
        self.igm.ig.add_action(Pid.PERSON_FOUND)
        self.igm.ig.add_action(Pid.SAY, args=["I found a human"])
        self.igm.ig.add_else()
        self.igm.ig.add_action(Pid.SAY, args=["No one is in front of me."])
        self.igm.ig.add_end_if()

        self.igm.ig.add_end_loop()

        self.igm.ig.add_action(Pid.SAY, args=["Hello new friend."])
        self.igm.ig.add_action(Pid.CLEANUP)
        self.igm.save_ig(self.ig_file_name)

    def run_instruction_graph(self):
        self.igm.load_ig(self.ig_file_name)
        self.igm.run()
