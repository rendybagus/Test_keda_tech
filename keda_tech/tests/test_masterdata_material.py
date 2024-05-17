from odoo.tests.common import TransactionCase

class TestMasterdataMaterial(TransactionCase):

    def setUp(self):
        super(TestMasterdataMaterial, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
        })

    def test_create_material_success(self):
        material = self.env['masterdata.material'].create({
            'name': 'Material Test',
            'code': 'M001',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.name, 'Material Test')
        self.assertEqual(material.code, 'M001')
        self.assertEqual(material.type, 'fabric')
        self.assertEqual(material.buy_price, 150)
        self.assertEqual(material.supplier_id, self.supplier)

    def test_create_material_fail_low_price(self):
        with self.assertRaises(Exception):
            self.env['masterdata.material'].create({
                'name': 'Material Test',
                'code': 'M001',
                'type': 'fabric',
                'buy_price': 50,  # Should raise an exception
                'supplier_id': self.supplier.id,
            })

    def test_update_material(self):
        material = self.env['masterdata.material'].create({
            'name': 'Material Test',
            'code': 'M001',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        material.write({'name': 'Updated Material'})
        self.assertEqual(material.name, 'Updated Material')

    def test_delete_material(self):
        material = self.env['masterdata.material'].create({
            'name': 'Material Test',
            'code': 'M001',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        material_id = material.id
        material.unlink()
        material_check = self.env['masterdata.material'].search([('id', '=', material_id)])
        self.assertFalse(material_check)
