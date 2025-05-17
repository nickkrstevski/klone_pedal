# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L
from faebryk.libs.units import P

class BridgeableModule(Module):
    input: F.ElectricSignal
    output: F.ElectricSignal

    @L.rf_field
    def can_bridge(self):
        return F.can_bridge_defined(self.input, self.output)
