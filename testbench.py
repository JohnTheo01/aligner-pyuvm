# type: ignore
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def hello_world(dut):
    """Simple hello world — clock + reset + signal init"""
    
    # Start 100MHz clock (10ns period)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    
    # Αρχικοποίηση όλων των inputs πριν το reset
    dut.paddr.value    = 0
    dut.pwrite.value   = 0
    dut.psel.value     = 0
    dut.penable.value  = 0
    dut.pwdata.value   = 0

    dut.md_rx_valid.value  = 0
    dut.md_rx_data.value   = 0
    dut.md_rx_offset.value = 0
    dut.md_rx_size.value   = 0

    dut.md_tx_ready.value = 0
    dut.md_tx_err.value   = 0

    # Reset sequence
    dut.reset_n.value = 1
    await Timer(3, unit="ns")
    
    dut.reset_n.value = 0
    await Timer(30, unit="ns")
    
    dut.reset_n.value = 1
    
    # Περίμενε 5 clock cycles μετά το reset
    for _ in range(5):
        await RisingEdge(dut.clk)
    
    dut._log.info("Reset sequence done!")