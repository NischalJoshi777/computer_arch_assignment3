from pathlib import Path
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import (
    obtain_resource,
)
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.X86, num_cores=1)

memory = SingleChannelDDR3_1600(size="1GB")

cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="512kB"
)

# Setup the board.
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the Full System workload from checkpoint
board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-5.4.49"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    checkpoint=  Path("/Users/nischaljsh/Documents/gem5/virtual"),
)

sim = Simulator(board=board, full_system=True)
print("Restoring from checkpoint and beginning simulation!")
sim.run()
print(
    "Exiting @ tick {} because {}.".format(
        sim.get_current_tick(),
        sim.get_last_exit_event_cause()
    )
)




# Modify TLB sizes after board initialization
def modify_tlb_sizes(board):
    for core in board.get_processor().get_cores():
        # Modify ITLB (Instruction TLB) size
        core.get_mmu().itb.size = 512  # Set to desired size
        core.get_mmu().dtb.size = 512  # Set to desired size
        core.get_mmu().page.size= "4KB"
        print(f"  ITLB size: {core.get_mmu().itb.size}")
        print(f"  DTLB size: {core.get_mmu().dtb.size}")


# Call the function to modify TLB sizes
modify_tlb_sizes(board)
