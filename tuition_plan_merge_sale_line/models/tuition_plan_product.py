#-*- coding:utf-8 -*-

from odoo import models, fields, api

class TuitionPlanProduct(models.Model):
    _inherit = "tuition.plan.product"

    merge_product_id = fields.Many2one(string="Merge With",
        comodel_name="product.product")

    @api.onchange("product_id")
    def _compute_merge_product_id(self):
        for line in self:
            if line.product_id:
                matched = False
                products = line.plan_id.product_ids.filtered(lambda l: l.product_id != line.product_id)
                if line.product_id.merge_product_ids:
                    for product in products:
                        if product.product_id in line.product_id.merge_product_ids:
                            line.merge_product_id = product.product_id.id
                            matched = True
                            break
                if not matched and line.product_id.merge_categ_ids:
                    for product in products:
                        if product.product_id.categ_id in line.product_id.merge_categ_ids:
                            line.merge_product_id = product.product_id.id
                            matched = True
                            break
                if not matched and len(line.product_id.merge_product_ids) == 1:
                    line.merge_product_id = line.product_id.merge_product_ids
    
    def _prepare_order_line_vals(self):
        self.ensure_one()
        res = super(TuitionPlanProduct, self)._prepare_order_line_vals()
        res["merge_product_id"] = self.merge_product_id.id
        return res