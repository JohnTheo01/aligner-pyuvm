# type: ignore
from pyuvm import *
from test.apb_pkg.apb_driver import ApbDriver
from test.apb_pkg.apb_monitor import ApbMonitor
from test.apb_pkg.apb_sequencer import ApbSequencer

class ApbAgent(uvm_agent):

    def build_phase(self):
        self.sequencer = ApbSequencer("sequencer", self)
        self.driver    = ApbDriver.create("driver", self)
        self.monitor   = ApbMonitor("monitor", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)