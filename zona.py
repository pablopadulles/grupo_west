from stdnum import get_cc_module
import stdnum.exceptions
from sql import Null, Column, Literal
from sql.functions import CharLength, Substring, Position

from trytond.i18n import gettext
from trytond.model import (ModelView, ModelSQL, MultiValueMixin, ValueMixin,
    DeactivableMixin, fields, Unique, sequence_ordered)
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pyson import Eval, Bool
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond import backend
from trytond.tools.multivalue import migrate_property
from trytond.tools import lstrip_wildcard
from .exceptions import (
    InvalidIdentifierCode, VIESUnavailable, SimilarityWarning, EraseError)

__all__ = ['Zona', 'Recorrido', 'RecorridoCliente']

class Zona(ModelSQL, ModelView):
    "Zona"
    __name__ = 'gwest.zona'

    name = fields.Char('Nombre', required=True)
    clientes = fields.One2Many('party.party', 'zona', 'Clientes',
            add_remove=[('categories', 'child_of', [3], 'parent')])


class Recorrido(ModelSQL, ModelView):
    "Recorridos de Cobrador"
    __name__ = 'gwest.recorrido'

    name = fields.Char('Codigo de Recorrido')
    zona = fields.Many2One('gwest.zona', 'Zona')
    cobrador = fields.Many2One('party.party', 'Cobrador',
            domain=[('categories', 'child_of', [2], 'parent')])
    fecha = fields.Date('Fecha')
    monto_recolectado = fields.Numeric('Monto Recolectado')
    clientes = fields.Many2Many('gwest.recorrido-party.party',
            'recorrido', 'party', 'Clientes',
            domain=[
                ('categories', 'child_of', [3], 'parent')
            ])

    @classmethod
    def __setup__(cls):
        super(Recorrido, cls).__setup__()
        cls._buttons.update({
            'crear_recorrido_zona': {'invisible': True}
            })

    @classmethod
    def crear_recorrido_zona(cls, recorridos):
        for recorrido in recorridos:
            #TODO hay que llenar el recorrido teniendo en cuenta la zona. Si ese campo esta bacio hay que borrar el contenido.
            # en clientes hay que poner los clientes que tiene que visitar.
            recorrido.save()

class RecorridoCliente(ModelSQL):
    'Recorrido - Cliente'
    __name__ = 'gwest.recorrido-party.party'
    _table = 'gwest_recorrido_party_party_rel'

    recorrido = fields.Many2One('gwest.recorrido', 'Recorrido', ondelete='CASCADE',
            select=True, required=True)
    party = fields.Many2One('party.party', 'Cliente', ondelete='RESTRICT',
            select=True, required=True)
