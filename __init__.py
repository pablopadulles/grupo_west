# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import gps
from . import party
from . import venta
from . import zona

def register():
    Pool.register(
        gps.GPS,
        party.Party,
        venta.Pago,
        venta.Venta,
        zona.Zona,
        module='grupo_west', type_='model')
    # Pool.register(
    #     party.CheckVIES,
    #     party.PartyReplace,
    #     party.PartyErase,
    #     module='party', type_='wizard')
