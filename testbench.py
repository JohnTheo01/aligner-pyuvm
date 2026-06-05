# type: ignore
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import pyuvm
from pyuvm import *
from env import AlgnEnv
from test.apb_pkg.apb_sequences import ApbWriteSequence, ApbReadSequence

@pyuvm.test()
class AlgnTest(uvm_test):

    def build_phase(self):
        self.env = AlgnEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        # Clock + Reset
        cocotb.start_soon(Clock(cocotb.top.clk, 10, unit="ns").start())

        cocotb.top.reset_n.value = 1
        await Timer(3, unit="ns")
        cocotb.top.reset_n.value = 0
        await Timer(30, unit="ns")
        cocotb.top.reset_n.value = 1

        for _ in range(5):
            await RisingEdge(cocotb.top.clk)

        # APB Write
        write_seq = ApbWriteSequence("write_seq")
        write_seq.addr = 0x0000
        write_seq.data = 0x12345678
        await write_seq.start(self.env.apb_agent.sequencer)

        # APB Read
        read_seq = ApbReadSequence("read_seq")
        read_seq.addr = 0x0000
        await read_seq.start(self.env.apb_agent.sequencer)

        self.logger.info(f"Read back: 0x{read_seq.result:08x}")

        self.drop_objection()