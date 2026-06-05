# type: ignore
from pyuvm import *
from enum import IntEnum

# APB direction
class ApbDir(IntEnum):
    READ  = 0
    WRITE = 1

# APB response
class ApbResponse(IntEnum):
    OKAY = 0
    ERR  = 1

# Base item
class ApbItemBase(uvm_sequence_item):
    def __init__(self, name="apb_item_base"):
        super().__init__(name)
        self.dir  = ApbDir.READ
        self.addr = 0
        self.data = 0

    def __str__(self):
        return f"dir: {self.dir.name}, addr: 0x{self.addr:04x}, data: 0x{self.data:08x}"

# Driver item
class ApbItemDrv(ApbItemBase):
    def __init__(self, name="apb_item_drv"):
        super().__init__(name)
        self.pre_drive_delay  = 0
        self.post_drive_delay = 0

    def __str__(self):
        return (f"{super().__str__()}, "
                f"pre_delay: {self.pre_drive_delay}, "
                f"post_delay: {self.post_drive_delay}")

# Monitor item
class ApbItemMon(ApbItemBase):
    def __init__(self, name="apb_item_mon"):
        super().__init__(name)
        self.response       = ApbResponse.OKAY
        self.length         = 0
        self.prev_item_delay = 0

    def __str__(self):
        return (f"{super().__str__()}, "
                f"response: {self.response.name}, "
                f"length: {self.length}, "
                f"prev_item_delay: {self.prev_item_delay}")