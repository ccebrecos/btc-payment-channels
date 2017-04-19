"""
Models a P2SH scriptSig, including the script with the conditions to spend
and the spend conditions such as signatures in multisig smart contracts,
secrets, etc...
"""
# Libraries
from .model import ScriptSig
from ...field.script import StackDataField


class P2SH(ScriptSig):
    """
    Models a pay to script hash scriptSig, containing in one side the reedem
    script payment values (signatures, secrets, ...) and the redeem script
    itself. The class allows to define separately the spend requirements and
    the redeem script so when serialized they are put together as in a P2SH,
    with the push data opcodes
    needed.

    Attributes:
        payment_script (Script): script with payment values
        reedem_script (ReedemScript): script with payment requirements
    """
    __slots__ = ["_payment_script", "_reedem_script"]

    def __init__(self, redeem_script, payment_script):
        self._payment_script = payment_script
        self._reedem_script = redeem_script

    def serialize(self):
        self._build()
        return super().serialize()

    def _build(self):
        """
        Serializes the P2SH scriptSig, by joining payment and redeem script
        """
        self._data = [self._payment_script, StackDataField(
            self._reedem_script.serialize())]

    @property
    def redeem_script(self):
        """ Returns the redeem script """
        return self._redeem_script

    @redeem_script.setter
    def redeem_script(self, script):
        """ Sets the redeem script """
        self._redeem_script = script

    @property
    def payment_script(self):
        """ Returns the payment script """
        return self._payment_script

    @payment_script.setter
    def payment_script(self, script):
        """ Sets the payment script """
        self._payment_script = script
