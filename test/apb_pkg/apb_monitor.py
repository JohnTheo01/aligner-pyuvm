# type: ignore
import cocotb
from pyuvm import *
from cocotb.triggers import RisingEdge
from test.apb_pkg.apb_items import ApbDir, ApbResponse, ApbItemMon

class ApbMonitor(uvm_component):

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def start_of_simulation_phase(self):
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            await self._collect_transaction()

    async def _collect_transaction(self):
        item = ApbItemMon()

        # Περίμενε για psel
        while self.dut.psel.value != 1:
            await RisingEdge(self.dut.clk)
            item.prev_item_delay += 1

        # Setup phase
        item.addr   = int(self.dut.paddr.value)
        item.dir    = ApbDir(int(self.dut.pwrite.value))
        item.length = 1

        if item.dir == ApbDir.WRITE:
            item.data = int(self.dut.pwdata.value)

        await RisingEdge(self.dut.clk)
        item.length += 1

        # Περίμενε για pready
        while self.dut.pready.value != 1:
            await RisingEdge(self.dut.clk)
            item.length += 1

        # Capture response
        item.response = ApbResponse(int(self.dut.pslverr.value))

        if item.dir == ApbDir.READ:
            item.data = int(self.dut.prdata.value)

        self.ap.write(item)
        self.logger.info(f"Monitored: {item}")

        await RisingEdge(self.dut.clk)