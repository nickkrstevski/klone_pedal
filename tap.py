import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L

class Tap(Module):
    tap: F.Electrical

    @L.rt_field
    def can_bridge(self):
        return F.can_bridge_defined(self.tap,self.tap)