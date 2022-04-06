
import unittest
import logging
from ..models.picking import Move
from ..models.picking import Picking
from ..models.res_company import ResCompany

_logger = logging.getLogger(__name__)

class TestInventory(unittest.TestCase):

    def setUp(self):
        print("setup")
        super(TestInventory, self).setUp()

        self.interval_time = self.env.ref('base.model_ir_cron')
        self.interval_time.write({'interval_number': 89})

    def tearDown(self):
        print("tearDown\n")


    def test_intervalNumber(self):
        time = self.interval_time
        self.assertEqual(time, 89)

        _logger.info("****************************************")


    def test_stock_move_validation(self):
        company = self.env.company.consignee_company_ids
        for compny in company:
            compny.with_context(comp_check=compny).update_stock()

        _logger.info(compny) 

    def test_consignee_stock(self):
        products = self.env['product.template']

        product_vals = {'name': 10103-1343,
                    'sale_ok': True,
                    'purchase_ok': True,
                    'is_garment': True,
                    'type': self.selection.product}

        company = self.env.company.consignee_company_ids

        if product_vals in products:
            if company in product_vals:
                move = company.with_context(comp_check=company).update_stock()
                _logger.info(move)
  

            
if __name__ == '__main__':
    unittest.main()  