import unittest
from machine import Pizza


class TestPizza(unittest.TestCase):
    def setUp(self) -> None:
        self.pizza = Pizza()

    def test_size_state(self):
        input_word = 'wrong'
        self.pizza.size()
        self.pizza.input(input_word)
        self.assertEqual(self.pizza.state, 'choose_size')

        input_word = 'большая'
        self.pizza.input('большая')
        self.assertEqual(self.pizza.state, 'choose_pay')
        self.assertEqual(self.pizza.chosen_size, input_word)

    def test_pay_state(self):

        self.pizza.to_choose_pay()
        self.pizza.input('wrong')
        self.assertEqual(self.pizza.state, 'choose_pay')

        self.pizza.input('карта')
        self.assertEqual(self.pizza.state, 'check')

    def test_check_state(self):
        self.pizza.to_check()
        self.pizza.input('да')
        self.assertEqual(self.pizza.state, 'final')

        self.pizza.to_check()
        self.pizza.input('нет')
        self.assertEqual(self.pizza.state, 'choose_size')
