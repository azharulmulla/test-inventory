import unittest
import logging

_logger = logging.getLogger(__name__)

class DefaultIntervalTimeTestCase(unittest.TestCase):
    def test_default_interval_time(self):
        default_time = self.env['ir.cron'].search([('interval_number', '==', 89),])
        self.assertEqual(default_time.size(), (89, 89))

        _logger.info("&&&&&&&&&&&&&&&&&&&&&&&&")
        _logger.info(default_time)
        _logger.info("&&&&&&&&&&&&&&&&&&&&&&&&")

    # def test_stock_move_time(self):
    #     move_time = self.env['ir.cron'].search([])
    #     if move_time > 89:
