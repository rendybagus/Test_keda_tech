from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MasterdataMaterial(models.Model):
    _name = 'masterdata.material'
    _description = 'Masterdata Material'

    name = fields.Char(string='Material Name', required=True)
    code = fields.Char(string='Material Code', required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('product_ready', 'Product Ready'),
        ('done', 'Done')
    ], string='Status', default='draft')
    po_id = fields.Many2one('purchase.order', string='Purchase Order')

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError('Buy price must be greater than 100')

    def action_check_material(self):
        if not self.env['product.product'].search([('barcode', '=', self.code)], limit=1):
            self.env['product.template'].create({
                'name': self.name,
                'barcode': self.code,
                'list_price': self.buy_price,
                'standard_price': self.buy_price,
            })
        self.write({'state': 'product_ready'})

    def action_create_po(self):
        po_id = self.env['purchase.order'].create({
            'partner_id': self.supplier_id.id,
            'order_line': [(0, 0, {
                'name': self.name,
                'product_qty': 1,
                'product_uom': 1,
                'price_unit': self.buy_price,
                'product_id': self.env['product.product'].search([('barcode', '=', self.code)], limit=1).id,
            })]
        })
        self.write({'state': 'done', 'po_id': po_id.id})
        return self.action_view_po()
        
    def action_view_po(self):
        return {
            'name': 'Purchase Order',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'res_id': self.po_id.id,
        }