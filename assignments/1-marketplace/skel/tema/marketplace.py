"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import time
import unittest
from logging.handlers import RotatingFileHandler
from threading import Lock, currentThread

import product as product_module


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # Lists of lists consisting of each consumers/producers products
        self.producers = []
        self.consumers = []

        # List with all the products available in the marketplace
        self.available_products = []

        # Locks
        self.producer_lock = Lock()
        self.consumer_lock = Lock()
        self.product_lock = Lock()

        # Logging initialisations
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Using Rotating File Handler as specified on ocw
        handler = RotatingFileHandler('marketplace.log')
        handler.setLevel(logging.INFO)

        # Setting a format for the logs
        formatter = logging.Formatter('%(asctime)s %(levelname)8s: %(message)s')
        handler.setFormatter(formatter)

        # Setting the time format
        logging.Formatter.converter = time.gmtime
        logger.addHandler(handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logger = logging.getLogger()
        logger.info("register producer")

        # Producer's index in the producers array = producer's id
        # Using lock in order not to have two producers with the same id
        with self.producer_lock:
            producer_id = len(self.producers)
            self.producers.append([])

        logger.info("registered producer %d", producer_id)
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace
        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        logger = logging.getLogger()
        logger.info("publish %s by %d", str(product), producer_id)

        # Using lock to avoid a race condition in case one consumer is trying to acquire a product
        # from a producer's array while he is trying to produce some other product
        with self.product_lock:
            # If the producer's array is full then he can't produce anymore and has to wait
            if len(self.producers[producer_id]) == self.queue_size_per_producer:
                logger.info("publishing %s by producer %d failed", str(product), producer_id)
                return False

            # Add the product to the producer's array and to the list of available products
            self.available_products.append(product)
            self.producers[producer_id].append(product)

        logger.info("publishing %s by producer %d succeeded", str(product), producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        logger = logging.getLogger()
        logger.info("new cart")

        # Consumer's index in the consumers array = cart's id
        # Using lock in order not to have two consumers with the same cart id
        with self.consumer_lock:
            cart_id = len(self.consumers)
            self.consumers.append([])

        logger.info("added cart %d", cart_id)
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again
        """
        logger = logging.getLogger()
        logger.info("add to cart %d %s", cart_id, str(product))

        # Using lock to avoid a race condition in case one consumer is trying to acquire a product
        # from a producer's array while he is trying to produce some other product
        with self.product_lock:
            # If the product isn't available at the moment in the marketplace the consumer has to
            # wait and try again later
            if product not in self.available_products:
                logger.info("adding %s to cart %d failed", str(product), cart_id)
                return False

            # Remove the product from the list of available products
            self.available_products.remove(product)

        # Add the product to the customer's cart
        self.consumers[cart_id].append(product)

        logger.info("adding %s to cart %d succeeded", str(product), cart_id)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        logger = logging.getLogger()
        logger.info("remove from cart %d %s", cart_id, str(product))

        # First check if the consumer is trying to remove a product that exists in his cart
        if product in self.consumers[cart_id]:
            # Remove the product from the cart and add it back to the list of available products
            self.consumers[cart_id].remove(product)

            with self.product_lock:
                self.available_products.append(product)

            logger.info("removing %s from cart %d succeeded", str(product), cart_id)
        else:
            logger.info("removing %s from cart %d failed", str(product), cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        logger = logging.getLogger()
        logger.info("place order from cart %d", cart_id)

        # Remove each product that the customer is buying from the producer's array in order for
        # him to produce other products
        for product in self.consumers[cart_id]:
            with self.product_lock:
                # Find which producer has the product the customer wants in its stock, then remove
                # it
                for id_producer in range(len(self.producers)):
                    if product in self.producers[id_producer]:
                        self.producers[id_producer].remove(product)

                print(currentThread().getName() + " bought " + str(product))

        # Empty the cart and place the order
        order = self.consumers[cart_id].copy()
        self.consumers[cart_id] = []

        logger.info("cart %d placed an order", cart_id)
        return order


class TestMarketplace(unittest.TestCase):
    """
    Class used for testing the Marketplace.
    """

    def setUp(self) -> None:
        """
        Sets up the testing environment for the unit tests.
        """
        self.marketplace = Marketplace(3)

        # Add a producer and a consumer
        self.producer = self.marketplace.register_producer()
        self.cart = self.marketplace.new_cart()

        # Add two products (The marketplace has a limit of 3 products per producer)
        self.marketplace.publish(self.producer,
                                 (product_module.Tea('Raspberry Tea', 1, 'Fruit'), 1, 0.05))
        self.marketplace.publish(self.producer,
                                 (product_module.Tea('Mint Tea', 2, 'Herbal'), 2, 0.12))

        # Add a product to the test consumer's cart
        self.marketplace.add_to_cart(self.cart,
                                     (product_module.Tea('Raspberry Tea', 1, 'Fruit'), 1, 0.05))

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
        self.assertEqual(
            self.marketplace.publish(self.producer,
                                     (product_module.Tea('Lime Tea', 5, 'Fruit'), 3, 0.1)), True)
        self.assertEqual(self.marketplace.publish(self.producer, (
            product_module.Tea('Camomile Tea', 1, 'Herbal'), 4, 0.16)), False)

    def test_add_to_cart(self):
        """
        Test the adding of a product from the Marketplace to a cart.
        """
        self.assertEqual(self.marketplace.add_to_cart(self.cart, (
            product_module.Tea('Mint Tea', 2, 'Herbal'), 2, 0.12)), True)

        # Trying to add a product that doesn't exist on the market
        self.assertEqual(self.marketplace.add_to_cart(self.cart, (
            product_module.Tea('Camomile Tea', 1, 'Herbal'), 4, 0.16)), False)

    def test_remove_from_cart(self):
        """
        Test the removing of a product from a cart.
        """
        self.assertEqual(self.marketplace.remove_from_cart(self.cart, (
            product_module.Tea('Raspberry Tea', 1, 'Fruit'), 1, 0.05)), None)
        self.assertListEqual(self.marketplace.place_order(self.cart), [], True)

        # Trying to remove a product that doesn't exist in the customer's cart
        self.assertEqual(self.marketplace.remove_from_cart(self.cart, (
            product_module.Tea('Lime Tea', 5, 'Fruit'), 3, 0.1)), None)
        self.assertListEqual(self.marketplace.place_order(self.cart), [], True)

    def test_place_order(self):
        """
        Test placing an order.
        """
        self.assertListEqual(self.marketplace.place_order(self.cart),
                             [(product_module.Tea('Raspberry Tea', 1, 'Fruit'), 1, 0.05)])
