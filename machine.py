from transitions import Machine, State
from abc import abstractmethod


class StateInterface(State):
    valid_words = []

    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def action(self, text, machine):
        pass


class Idle(StateInterface):

    def action(self, text, machine):
        if text.lower() == 'go':
            machine.size()


class ChooseSize(StateInterface):
    valid_words = ['большая', 'маленькая']

    def action(self, text, machine):
        if text.lower() in self.valid_words:
            machine.chosen_size = text
            machine.pay()


class ChoosePay(StateInterface):
    valid_words = ['наличные', 'карта']

    def action(self, text, machine):
        if text.lower() in self.valid_words:
            machine.chosen_pay = text
            machine.check()


class Check(StateInterface):

    def action(self, text, machine):
        if text.lower() == 'да':
            machine.final()
        elif text.lower() == 'нет':
            machine.clean()
            machine.to_choose_size()


class Final(StateInterface):

    def action(self, text, machine):
        if text.lower() == 'go':
            machine.clean()
            machine.to_choose_size()


class Pizza(Machine):
    states = [Idle('idle'), ChooseSize('choose_size'), ChoosePay('choose_pay'), Check('check'), Final('final')]
    transition = [
        ['size', 'idle', 'choose_size'],
        ['pay', 'choose_size', 'choose_pay'],
        ['check', 'choose_pay', 'check'],
        ['final', 'check', 'final']
    ]

    def __init__(self):
        super().__init__(model=self,
                         states=self.__class__.states,
                         transitions=self.__class__.transition,
                         initial='idle')
        self.input_text = ''
        self.output_text = ''
        self.chosen_size = ''
        self.chosen_pay = ''
        self.on_enter_idle()

    def input(self, text):
        return self.get_state(self.state).action(text, self)

    def clean(self):
        self.chosen_pay = ''
        self.chosen_size = ''

    def on_enter_idle(self):
        self.output_text = 'Введите go, чтобы заказать пиццу'

    def on_enter_choose_size(self):
        self.output_text = 'Большая, или маленькая'

    def on_enter_choose_pay(self):
        self.output_text = 'наличные, или карта'

    def on_enter_check(self):
        self.output_text = f'Ваш заказ - {self.chosen_size} пицца, оплата {self.chosen_pay}.' \
                           f' Введите да, чтобы подтвердить, или нет чтобы изменить параметры'

    def on_enter_final(self):
        self.output_text = 'Ваш заказ передан в доставку. Введите go, чтобы сделать еще один'
