import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L

class Bridgeable(Module):
    input: F.ElectricSignal
    output: F.ElectricSignal

    @L.rt_field
    def can_bridge(self):
        return F.can_bridge_defined(self.input,self.output)