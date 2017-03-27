"""
Defines a class to model a P2PKH address, this means, adding extra methods to
validate the checksum when deserializing or decoding and properties to later
get the public key hash from the address using the data property
"""
# Libraries
from .model import Address
from .types import Types
from .helper import DOUBLESHA256_CHECKSUM_SIZE, doublesha256_checksum,\
    doublesha256_checksum_validate, ripemd160_sha256

# Constants
PREFIX_SIZE = 1
"""
    int: size in bytes of the P2PKH prefixes
"""
PKH_SIZE = 20
"""
    int: size in bytes of all public key hashes
"""
CHECKSUM_SIZE = DOUBLESHA256_CHECKSUM_SIZE
"""
    int: size in bytes for the address suffix checksum
"""
ADDRESS_SIZE = PREFIX_SIZE + PKH_SIZE + CHECKSUM_SIZE
"""
    int: size in byte of the P2PKH addresses
"""


# Classes
class P2PKH(Address):
    """
    Pay to public key hash address. Allows to serialize, deserialize, encode
    and decode P2PKH addresses so the public key hash can be easily set and
    got to generate / decode easily P2PKH addresses, as checksum calculations
    are performed automagically
    """
    __slots__ = ["_pkh"]

    def __init__(self, addr_net, public_key=None, public_key_hash=None,
                 value=None):
        """
        Creates a P2PKH specifying the network and public key or public key
        hash. Also provides the ability to provide the public key hash and
        checksum (value)

        If both public key and public key hash are given, just the public
        key hash is set and public key is ignored. If value is also provided,
        then value is picked first

        Args:
            addr_net (Network): network where the P2PKH operates
            public_key (bytes): public key to generate public key hash from
            public_key_hash (bytes): public key hash of the address
            value (bytes): data of the address containing the public key hash
            and checksum
        """
        # Type assertions
        assert isinstance(public_key, bytes) or public_key is None, """Public
        key must be a bytes object"""
        assert isinstance(public_key_hash, bytes) or public_key_hash is None, \
            """Public key hash must be a bytes object"""
        assert isinstance(value, bytes) or value is None, \
            """Value of the P2PKH address must be a bytes object"""
        assert public_key is not None or public_key_hash is not None \
            or value is not None, """To create a P2PKH address you must
            specify either a public key or public key hash"""

        # Initialize
        super().__init__(Types.p2pkh, addr_net)

        # Direct value set
        if value is not None:
            self._value = value
        else:
            # Obtain public key hash and set
            if public_key_hash is not None:
                if len(public_key_hash) != PKH_SIZE:
                    raise ValueError("""Unable to set a public key hash with
                    length %d bytes. Public key hash has to be %d bytes""" % (
                        len(public_key_hash), PKH_SIZE))
            elif public_key is not None:
                public_key_hash = ripemd160_sha256(public_key)
            # Update value
            self._value = public_key_hash + doublesha256_checksum(
                self._prefix + public_key_hash)

    @classmethod
    def deserialize(cls, address):
        """
        Deserializes the given address as an array of bytes, guessing its
        prefix and saving its info, checking that the prefix type is P2PKH and
        after that, setting the public key hash value

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            cls: a new object containing the P2PKH address
        """
        # Check size
        if len(address) != ADDRESS_SIZE:
            raise ValueError("""P2PKH Address %s size in bytes is not valid.
        All P2PKH addresses have %d bytes""" % (address.hex(), ADDRESS_SIZE))
        # Basic deserialization
        addr = Address.deserialize(address)
        # Check type is correct
        if addr.type != Types.p2pkh:
            raise ValueError("""The deserialized address is not a P2PKH
            address""")
        return cls(addr.network, value=addr.value)

    @property
    def pkh(self):
        """ Extracts the public key hash from the address """
        return self._value[:-CHECKSUM_SIZE]

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]
