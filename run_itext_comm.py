from instruction_graph.interactive.InteractiveManager import InteractiveManager
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.interactive.TextCommunicator import TextCommunicator


library = ExamplePrimitiveLibrary()
memory = DefaultMemory()
im = InteractiveManager(library=library, memory=memory)

tc = TextCommunicator(im)

tc.run()


