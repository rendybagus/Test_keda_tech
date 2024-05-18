import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request

class MasterdataMaterialControllerRestApi(http.Controller):
    @http.route('/api/masterdata/material/', type='http', auth='public', methods=['GET'], csrf=False)
    def get_masterdata_material(self, **kw):
        try:
            if kw.get('id'):
                materials = request.env['masterdata.material'].sudo().search([('id', '=', kw.get('id'))], limit=1)
            else:
                materials = request.env['masterdata.material'].sudo().search([])
            data = [{
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier': material.supplier_id.name,
                'state': material.state,
            } for material in materials]

            response_data = {
                'status': 200,
                'message': 'Success',
                'data': data
            }
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json; charset=utf-8',
                response=json.dumps(response_data)
            )
        except Exception as e:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'status': 400,
                    'message': str(e)
                })
            )

    @http.route('/api/masterdata/material/', type='json', auth='public', methods=['POST'], csrf=False)
    def post_masterdata_material(self, **params):
        print(params)
        try:
            if params.get('buy_price') < 100:
                raise Exception('Buy price must be greater than 100')
            material = request.env['masterdata.material'].sudo().create({
                'name': params.get('name'),
                'code': params.get('code'),
                'type': params.get('type'),
                'buy_price': params.get('buy_price'),
                'supplier_id': params.get('supplier_id'),
            })

            data = {
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier': material.supplier_id.name,
                'state': 'draft',
            }

            response_data = {
                'status': 200,
                'message': 'Success POST',
                'data': data
            }
            return response_data
        except Exception as e:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'status': 400,
                    'message': str(e)
                })
            )

    @http.route('/api/masterdata/material/', type='json', auth='public', methods=['PUT'], csrf=False)
    def put_masterdata_material(self, **params):
        try:
            material = request.env['masterdata.material'].sudo().search([('id', '=', params.get('id'))], limit=1)
            if material:
                material.write({
                    'name': params.get('name'),
                    'code': params.get('code'),
                    'type': params.get('type'),
                    'buy_price': params.get('buy_price'),
                    'supplier_id': params.get('supplier_id'),
                })

                data = {
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier': material.supplier_id.name,
                }

                response_data = {
                    'status': 200,
                    'message': 'Success PUT',
                    'data': data
                }
                return response_data
            else:
                raise Exception('Material not found')
        except Exception as e:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'status': 400,
                    'message': str(e)
                })
            )

    @http.route('/api/masterdata/material/', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_masterdata_material(self, **params):
        try:
            material = request.env['masterdata.material'].sudo().search([('id', '=', params.get('id'))], limit=1)
            if material:
                material.unlink()
                response_data = {
                    'status': 200,
                    'message': 'Success DELETE',
                }
                return response_data
            else:
                raise Exception('Material not found')
        except Exception as e:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'status': 400,
                    'message': str(e)
                })
            )
