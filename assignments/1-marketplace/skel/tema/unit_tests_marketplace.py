import unittest

import marketplace


class TestMarketplaceMethods(unittest.TestCase):
    """
    Class used for testing the Marketplace.
    """

    def setUp(self) -> None:
        """
        Sets up the testing environment for the unit tests.
        """
        self.marketplace = marketplace.Marketplace(3)

        self.producer = self.marketplace.register_producer()
        self.cart = self.marketplace.new_cart()

        self.marketplace.publish(self.producer, ('Raspberry Tea', 1, 0.05))
        self.marketplace.publish(self.producer, ('Mint Tea', 2, 0.12))

        self.marketplace.add_to_cart(self.cart, ('Raspberry Tea', 1, 0.05))

    def test_register_producer(self):
        """
        Test the registration of a producer in the Marketplace.
        """
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)

    def test_new_cart(self):
        """
        Test the registration of a consumer in the Marketplace.
        """
        self.assertEqual(self.marketplace.new_cart(), 1)
        self.assertEqual(self.marketplace.new_cart(), 2)

    def test_publish(self):
        """
        Test the publishing of a product in the Marketplace.
        """
        self.assertEqual(self.marketplace.publish(self.producer, ('Lime Tea', 3, 0.1)), True)
        self.assertEqual(self.marketplace.publish(self.producer, ('Camomile Tea', 4, 0.16)), False)

    def test_add_to_cart(self):
        """
        Test the adding of a product from the Marketplace to a cart.
        """
        self.assertEqual(self.marketplace.add_to_cart(self.cart, ('Mint Tea', 2, 0.12)), True)
        self.assertEqual(self.marketplace.add_to_cart(self.cart, ('Camomile Tea', 4, 0.16)), False)

    def test_remove_from_cart(self):
        """
        Test the removing of a product a cart.
        """
        self.assertEqual(self.marketplace.remove_from_cart(self.cart,
                                                           ('Raspberry Tea', 1, 0.05)), None)
        self.assertListEqual(self.marketplace.place_order(self.cart), [], True)

        self.assertEqual(self.marketplace.remove_from_cart(self.cart, ('Lime Tea', 3, 0.1)), None)
        self.assertListEqual(self.marketplace.place_order(self.cart), [], True)

    def test_place_order(self):
        """
        Test placing an order.
        """
        self.assertListEqual(self.marketplace.place_order(self.cart), [('Raspberry Tea', 1, 0.05)])
