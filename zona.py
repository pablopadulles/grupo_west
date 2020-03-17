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

    name = fields.Char('Codigo de Recorrido', readonly=True)
    zona = fields.Many2One('gwest.zona', 'Zona')
    cobrador = fields.Many2One('party.party', 'Cobrador',
            domain=[('categories', 'child_of', [2], 'parent')])
    fecha = fields.Date('Fecha', states={'required': True})
    monto_recolectado = fields.Numeric('Monto Recolectado', states={'readonly': True})
    clientes = fields.Many2Many('gwest.recorrido-party.party',
            'recorrido', 'party', 'Clientes',
            domain=[
                ('categories', 'child_of', [3], 'parent')
            ])

    @classmethod
    def __setup__(cls):
        super(Recorrido, cls).__setup__()
        cls._buttons.update({
            'crear_recorrido_zona': {'invisible': False}
            })

    @classmethod
    def crear_recorrido_zona(cls, recorridos):
        for recorrido in recorridos:
            clientes = list(recorrido.clientes)
            if recorrido.zona:
                for cliente in recorrido.zona.clientes:
                    clientes.append(cliente)
                recorrido.clientes = clientes
            else:
                recorrido.clientes = None
            recorrido.save()

    @classmethod
    def _new_code(cls, **pattern):
        pool = Pool()
        Sequence = pool.get('ir.sequence')
        Configuration = pool.get('gwest.sequences')
        config = Configuration(1)
        sequence = config.get_multivalue('recorrido_sequence', **pattern)
        if sequence:
            return Sequence.get_id(sequence.id)

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls._new_code()
        return super(Recorrido, cls).create(vlist)


class RecorridoCliente(ModelSQL):
    'Recorrido - Cliente'
    __name__ = 'gwest.recorrido-party.party'
    _table = 'gwest_recorrido_party_party_rel'

    recorrido = fields.Many2One('gwest.recorrido', 'Recorrido', ondelete='CASCADE',
            select=True, required=True)
    party = fields.Many2One('party.party', 'Cliente', ondelete='RESTRICT',
            select=True, required=True)
