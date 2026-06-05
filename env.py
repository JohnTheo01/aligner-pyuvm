# type: ignore
from pyuvm import *
from test.apb_pkg.apb_agent import ApbAgent

class AlgnEnv(uvm_env):

    def build_phase(self):
        self.apb_agent = ApbAgent("apb_agent", self)

    def connect_phase(self):
        pass