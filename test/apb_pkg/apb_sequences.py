# type: ignore
from pyuvm import *
from test.apb_pkg.apb_items import ApbDir, ApbItemDrv

class ApbSequenceBase(uvm_sequence):
    pass

class ApbWriteSequence(ApbSequenceBase):
    def __init__(self, name="apb_write_seq"):
        super().__init__(name)
        self.addr = 0
        self.data = 0

    async def body(self):
        item = ApbItemDrv("item")
        item.dir  = ApbDir.WRITE
        item.addr = self.addr
        item.data = self.data

        await self.start_item(item)
        await self.finish_item(item)

        print(f"Write: addr=0x{self.addr:04x} data=0x{self.data:08x}")

class ApbReadSequence(ApbSequenceBase):
    def __init__(self, name="apb_read_seq"):
        super().__init__(name)
        self.addr   = 0
        self.result = 0

    async def body(self):
        item = ApbItemDrv("item")
        item.dir  = ApbDir.READ
        item.addr = self.addr

        await self.start_item(item)
        await self.finish_item(item)

        self.result = item.data
        print(f"Read: addr=0x{self.addr:04x} data=0x{self.result:08x}")