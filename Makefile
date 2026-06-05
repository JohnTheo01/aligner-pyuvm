CWD=$(shell pwd)

SIM ?= icarus
TOPLEVEL_LANG = verilog

# DUT sources
VERILOG_SOURCES = $(CWD)/src/cfs_aligner.v \
                  $(CWD)/src/cfs_aligner_core.v \
                  $(CWD)/src/cfs_ctrl.v \
                  $(CWD)/src/cfs_rx_ctrl.v \
                  $(CWD)/src/cfs_tx_ctrl.v \
                  $(CWD)/src/cfs_regs.v \
                  $(CWD)/src/cfs_synch.v \
                  $(CWD)/src/cfs_synch_fifo.v \
                  $(CWD)/src/cfs_edge_detect.v

TOPLEVEL = cfs_aligner
MODULE   = testbench

COCOTB_HDL_TIMEUNIT      = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include $(shell cocotb-config --makefiles)/Makefile.sim