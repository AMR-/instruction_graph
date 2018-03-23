#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
from instruction_graph.example.pepper_utils import init_qi_controller
from PepperController import Controller

control = init_qi_controller(Controller)

control.build_instruction_graph()
