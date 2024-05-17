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

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError('Buy price must be greater than 100')