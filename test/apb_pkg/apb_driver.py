# type: ignore
import cocotb
from pyuvm import *
from cocotb.triggers import RisingEdge
from test.apb_pkg.apb_items import ApbDir, ApbItemDrv

class ApbDriver(uvm_driver):

    def start_of_simulation_phase(self):
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            await self._drive_transaction(item)
            self.seq_item_port.item_done()

    async def _drive_transaction(self, item: ApbItemDrv):
        # Pre drive delay
        for _ in range(item.pre_drive_delay):
            await RisingEdge(self.dut.clk)

        # Setup phase
        self.dut.psel.value   = 1
        self.dut.pwrite.value = int(item.dir)
        self.dut.paddr.value  = item.addr

        if item.dir == ApbDir.WRITE:
            self.dut.pwdata.value = item.data

        await RisingEdge(self.dut.clk)

        # Enable phase
        self.dut.penable.value = 1

        await RisingEdge(self.dut.clk)

        # Wait for pready
        while self.dut.pready.value != 1:
            await RisingEdge(self.dut.clk)

        # Deassert signals
        self.dut.psel.value    = 0
        self.dut.penable.value = 0
        self.dut.pwrite.value  = 0
        self.dut.paddr.value   = 0
        self.dut.pwdata.value  = 0

        self.logger.info(f"Drove: {item}")

        # Post drive delay
        for _ in range(item.post_drive_delay):
            await RisingEdge(self.dut.clk)