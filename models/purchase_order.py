# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    data_wb_supplier = fields.Boolean(
        related='partner_id.data_wb_supplier', 
        string='¿Es proveedor?',
        store=True # Recomendado guardar store=True si se usa en dominios de búsqueda frecuentes
    )
    
    # ---------------------------------------------------------------------------------
    # Nuevos campos Odoo 18.0 
    # --- FECHAS Y TIEMPOS ---
    data_fecha_carga_tracking = fields.Datetime(string='Fecha carga al tracking')
    data_exfty = fields.Datetime(string='EXFTY', help='Fecha de carga lista')
    data_fecha_anticipo = fields.Datetime(string='FECHA ANTICIPO')
    data_etd = fields.Datetime(string='ETD', help='Estimated time of departure / Fecha estimada de zarpe')
    data_eta = fields.Datetime(string='ETA', help='Estimated time of arrival / Fecha estimada de arribo')
    data_atd = fields.Datetime(string='ATD', help='Actual time of departure / Dia de zarpe real')
    data_ata = fields.Datetime(string='ATA', help='Actual time of arrival / Dia de arribo real')
    data_notificacion_arribo = fields.Datetime(string='NOTIFICACIÓN DE ARRIBO', help='Dia de notificacion de Arribo a POD')
    data_fecha_despacho = fields.Datetime(string='FECHA DE DESPACHO')
    data_fecha_cedis = fields.Datetime(string='FECHA CEDIS', help='CEDIS = Centro de distribucion=Tlane')
    data_fecha_factura = fields.Datetime(string='FECHA FACTURA')
    
    data_tdt = fields.Integer(string='TdT [días]', help='Tiempo de Tránsito')

    # --- CARGA Y CONTENEDOR ---
    
    # Quitamos estos apetición de "compras" porque son automáticos.
    #data_loading_hq = fields.Integer(string='Loading HQ', help='Cupo en unidades en un contenedor')
    #data_loading_percentage = fields.Float(string='Loading %', help='% que ocupa de un Contenedor 40HQ')
    # ------------------------------------------------------------------------------------------------------
    data_contenedor = fields.Char(string='CONTENEDOR', help='Clave identificadora de contenedor, cada contenedor es separado por una coma')
    data_telex = fields.Boolean(string='TELEX?', help='Si o No el telex esta ejecutado')

    # --- FINANZAS Y ADUANA ---
    data_bonificacion = fields.Float(
        string='Bonificación (+ o -)', 
        help='En caso de diferencias entre ordenado y recibido...'
    )
    
    data_factura_comercial = fields.Char(string='FACTURA COMERCIAL')
    data_tc = fields.Float(string='TC', digits=(12, 4), help='Tipo de cambio') # digits=(12,4) es estándar para TC
    data_arancel = fields.Float(string='Arancel', help='IGI en Pedimento')

    # --- CONTROL Y COMENTARIOS ---
    data_comentarios = fields.Text(string='COMENTARIOS')
    #data_status_last_update = fields.Char(string='Status Last Update')
    #data_status_last_user_update = fields.Char(string='Status Last User Update')

    # --- CAMPOS RELACIONALES (MANY2ONE) ---
    data_pol_id = fields.Many2one('purchase.port', string='POL', help='Puerto de carga en origen')
    data_pod_id = fields.Many2one('purchase.port', string='POD', help='Puerto de descarga en destino')
    data_status_po_id = fields.Many2one('purchase.status.po', string='STATUS', help='Fase de la PO')
    data_agente_aduanal_id = fields.Many2one('purchase.agente.aduanal', string='AA', help='Agente Aduanal')
    data_forwarder_id = fields.Many2one('purchase.forwarder', string='FORWARDER', help='Proveedor logístico marítimo')
    data_naviera_id = fields.Many2one('purchase.naviera', string='NAVIERA', help='Operadora de Flete Maritima')
    data_terrestre_id = fields.Many2one('purchase.terrestre', string='TERRESTRE', help='Operador Terrestre')
    data_clave_pedimento_id = fields.Many2one('purchase.clave.pedimento', string='Clave de Pedimento')
    data_status_entrega_id = fields.Many2one('purchase.status.entrega', string='STATUS ENTREGA')
    data_comprador_id = fields.Many2one('res.users', string='COMPRADOR') # Recomiendo enlazarlo a los usuarios de Odoo
    data_nrs_id = fields.Many2one('purchase.nrs', string='N/R/S', help='Nuevo/Resurtido/Sustituto (Cambio de aspecto)')
    data_nrs_color = fields.Integer(string='Color N/R/S')
    
    def action_bonification_calculate(self):
        self.ensure_one()
        
        total_bonification = 0.0
        # Iteramos sobre las líneas de ESTA orden de compra específica
        for line in self.order_line:
            #FÓRMULA MATEMÁTICA
            # Ejemplo temporal:
            # diferencia = line.product_qty - line.qty_received
            # total_bonificacion += diferencia
            pass 
            
        # Al final del ciclo, asignamos el total al campo de la orden
        self.data_bonificacion = total_bonification
        
    

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# MODELOS DE CATÁLOGOS (Listas de opciones)


class PurchasePort(models.Model):
    _name = 'purchase.port'
    _description = 'Puerto de Carga / Descarga'
    
    name = fields.Char(string='Nombre del Puerto', required=True)

class PurchaseStatusPO(models.Model):
    _name = 'purchase.status.po'
    _description = 'Fase de la PO'
    
    name = fields.Char(string='Status', required=True)

class PurchaseAgenteAduanal(models.Model):
    _name = 'purchase.agente.aduanal'
    _description = 'Agente Aduanal'
    
    name = fields.Char(string='Agente Aduanal', required=True)

class PurchaseForwarder(models.Model):
    _name = 'purchase.forwarder'
    _description = 'Proveedor Logístico Marítimo'
    
    name = fields.Char(string='Forwarder', required=True)

class PurchaseNaviera(models.Model):
    _name = 'purchase.naviera'
    _description = 'Operadora de Flete Marítima'
    
    name = fields.Char(string='Naviera', required=True)

class PurchaseTerrestre(models.Model):
    _name = 'purchase.terrestre'
    _description = 'Operador Terrestre'
    
    name = fields.Char(string='Operador Terrestre', required=True)

class PurchaseClavePedimento(models.Model):
    _name = 'purchase.clave.pedimento'
    _description = 'Clave de Pedimento'
    
    name = fields.Char(string='Clave', required=True)

class PurchaseStatusEntrega(models.Model):
    _name = 'purchase.status.entrega'
    _description = 'Status de Entrega'
    
    name = fields.Char(string='Status de Entrega', required=True)

class PurchaseNRS(models.Model):
    _name = 'purchase.nrs'
    _description = 'N/R/S (Nuevo/Resurtido/Sustituto)'
    
    name = fields.Char(string='Nombre', required=True)
    