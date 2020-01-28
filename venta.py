import copy
import logging
from decimal import Decimal

from sql import Null, Column

from trytond.model import (
    ModelView, ModelSQL, Model, UnionMixin, DeactivableMixin, fields)
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond import backend
from trytond.config import config
from trytond.tools import lstrip_wildcard
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Venta']

class Venta(ModelSQL, ModelView):
    "Ventas"
    __name__ = "gwest.venta"

    name = fields.Many2One('product.product', 'Producto')
    precio = fields.Numeric('Precio Venta')
    cuotas = fields.Integer('Cantidad Cuotas')
    pagos = fields.One2Many('gwest.pago', 'name', 'Pagos')
    restante = fields.Function(fields.Numeric('Resta Abonar'), 'get_restante')
    pago_parcial = fields.Function(fields.Numeric('Parcial Abonado'), 'get_pago_parcial')
    cliente = fields.Many2One('party.party', 'Cliente')

    def get_restante(self, name):
        return Decimal('999')

    def get_pago_parcial(self, name):
        return Decimal('999')


class Pago(ModelSQL, ModelView):
    "Pago"
    __name__ = "gwest.pago"

    name = fields.Many2One('gwest.venta', 'Venta')
    pago = fields.Numeric('Monto')


