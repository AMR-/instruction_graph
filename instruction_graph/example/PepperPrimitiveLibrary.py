from instruction_graph import BasePrimitiveLibrary
from instruction_graph import ActionPrimitive as Action, ConditionalPrimitive as Cond
from PepperMemory import States


class PepperPrimitiveLibrary(BasePrimitiveLibrary):
    def list_action_primitives(self):
        return [
            Action(PrimitiveIds.SAY, self.say, "Say", "Perform text to speech on the input argument"),
            Action(PrimitiveIds.ROTATE, self.rotate),
            Action(PrimitiveIds.PERSON_FOUND, self.mark_person_found),
            Action(PrimitiveIds.CLEANUP, self.cleanup),
        ]

    def list_conditional_primitives(self):
        return [
            Cond(PrimitiveIds.IS_SEARCHING, self.is_pepper_searching),
            Cond(PrimitiveIds.IS_HUMAN_VISIBLE, self.is_human_visible)
        ]

    def library_name(self):
        return "Pepper_Example_Primitive_Library"

    @staticmethod
    def say(memory, text):
        tts = memory.session.service("ALTextToSpeech")
        tts.say(text)

    @staticmethod
    def rotate(memory, direction, radians):
        if direction not in ['R', "L"]:
            raise ValueError("'direction' should be 'R' or 'L'")
        fraction_max_speed = 0.3
        turn = (-1)*radians if direction is 'R' else radians
        joint_name = "Body"
        motion = memory.session.service("ALMotion")
        motion.changeAngles(joint_name, turn, fraction_max_speed)

    @staticmethod
    def mark_person_found(memory):
        memory.state = States.FOUND_PERSON

    @staticmethod
    def cleanup(memory):
        memory.cleanup()

    @staticmethod
    def is_pepper_searching(memory):
        return memory.state == States.SEARCHING

    @staticmethod
    def is_human_visible(memory):
        mem_proxy = memory.session.service("ALMemory")
        val = mem_proxy.getData("FaceDetected", 0)
        if val and isinstance(val, list) and len(val) == 2:
            print("this is the val")
            print (val)
            return True
        else:
            print("Nope, this is the val")
            print(val)
            return False


# noinspection PyClassHasNoInit
class PrimitiveIds:
    SAY = "say"
    ROTATE = "rotate"
    PERSON_FOUND = "change_state_to_person_found"
    CLEANUP = "cleanup"

    IS_SEARCHING = "is_pepper_searching"
    IS_HUMAN_VISIBLE = "is_human_visible"
