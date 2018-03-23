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
        angles = [0, 0, radians if 'L' else -radians]
        motion = memory.session.service("ALMotion")
        motion.moveTo(angles)

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
        human_data_exists = (val is not None and isinstance(val, list) and len(val) == 5)
        return human_data_exists


# noinspection PyClassHasNoInit
class PrimitiveIds:
    SAY = "say"
    ROTATE = "rotate"
    PERSON_FOUND = "change_state_to_person_found"
    CLEANUP = "cleanup"

    IS_SEARCHING = "is_pepper_searching"
    IS_HUMAN_VISIBLE = "is_human_visible"
