#!/usr/bin/env python
from instruction_graph.interactive.InteractiveManager import InteractiveManager
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.interactive.TextCommunicator import TextCommunicator


if __name__ == "__main__":
    library = ExamplePrimitiveLibrary()
    memory = DefaultMemory()
    im = InteractiveManager(library=library, memory=memory)
    tc = TextCommunicator(im)
    tc.run()
