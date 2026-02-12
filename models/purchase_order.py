# -*- coding: utf-8 -*-
from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    data_wb_supplier = fields.Boolean(
        related='partner_id.data_wb_supplier', 
        string='¿Es proveedor?',
        store=True # Recomendado guardar store=True si se usa en dominios de búsqueda frecuentes
    )