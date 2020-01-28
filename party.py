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

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    lastname = fields.Char('Apellido', select=True)
    gpss = fields.One2Many('gwest.gps', 'party', 'GPS')
    zona = fields.Many2One('gwest.zona', 'Zona', select=True)
    parent = fields.Many2One('party.party', 'Vendedor', select=True)
    childs = fields.One2Many('party.party', 'parent', 'Clientes')
    dni = fields.Char('DNI')
    foto = fields.Binary('Binary')
    productos = fields.One2Many('gwest.venta', 'cliente', 'Compras')
