import unittest

import marketplace


class TestMarketplaceMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.marketplace = marketplace.Marketplace(3)

        self.producer = self.marketplace.register_producer()
        self.cart = self.marketplace.new_cart()

        self.marketplace.publish(self.producer, ('Raspberry Tea', 1, 0.05))
        self.marketplace.publish(self.producer, ('Mint Tea', 2, 0.12))

        self.marketplace.add_to_cart(self.cart, ('Raspberry Tea', 1, 0.05))

    def test_register_producer(self):
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)

    def test_new_cart(self):
        self.assertEqual(self.marketplace.new_cart(), 1)
        self.assertEqual(self.marketplace.new_cart(), 2)

    def test_publish(self):
        self.assertEqual(self.marketplace.publish(self.producer, ('Lime Tea', 3, 0.1)), True)
        self.assertEqual(self.marketplace.publish(self.producer, ('Camomile Tea', 4, 0.16)), False)

    def test_add_to_cart(self):
        self.assertEqual(self.marketplace.add_to_cart(self.cart, ('Mint Tea', 2, 0.12)), True)
        self.assertEqual(self.marketplace.add_to_cart(self.cart, ('Camomile Tea', 4, 0.16)), False)

    def test_remove_from_cart(self):
        self.assertEqual(self.marketplace.remove_from_cart(self.cart, ('Raspberry Tea', 1, 0.05)), None)
        self.assertEqual(self.marketplace.remove_from_cart(self.cart, ('Lime Tea', 3, 0.1)), None)

    def test_place_order(self):
        self.assertListEqual(list(self.marketplace.place_order(self.cart)), [('Raspberry Tea', 1, 0.05)])