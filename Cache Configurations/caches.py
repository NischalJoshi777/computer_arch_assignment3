from m5.objects import Cache

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    def __init__(self, size="32kB", assoc=2):
        super().__init__()
        self.size = size
        self.assoc = assoc

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        raise NotImplementedError

# L1 Instruction Cache Class
class L1ICache(L1Cache):
    def __init__(self, size="32kB", assoc=2):
        super().__init__(size=size, assoc=assoc)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

# L1 Data Cache Class
class L1DCache(L1Cache):
    def __init__(self, size="64kB", assoc=2):
        super().__init__(size=size, assoc=assoc)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

# L2 Cache Class
class L2Cache(Cache):
    def __init__(self, size="256kB", assoc=16):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = 20
        self.data_latency = 20
        self.response_latency = 20
        self.mshrs = 20
        self.tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
