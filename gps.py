from trytond.model import (
    ModelView, ModelSQL, DeactivableMixin, fields, Exclude, tree)
from trytond.pyson import Eval

__all__ = ['GPS']

class GPS(ModelSQL, ModelView):
    "GPS"
    __name__ = 'gwest.gps'

    party = fields.Many2One('party.party', "Cobrador", ondelete='CASCADE',
            required=True, select=True)
    latitud = fields.Char('Latitud')
    longitud = fields.Char('Longitud')
    fecha_hora = fields.DateTime('Fecha Hora')

    @classmethod
    def __setup__(cls):
        super(GPS, cls).__setup__()
        cls._order.insert(0, ('fecha_hora', 'ASC'))
