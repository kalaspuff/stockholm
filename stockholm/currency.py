import sys
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union, cast


class MetaCurrency(type):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]
    _meta: bool

    def __new__(cls, name: str, bases: Tuple[type, ...], attributedict: Dict) -> "MetaCurrency":
        ticker = attributedict.get("ticker", attributedict.get("__qualname__"))
        decimal_digits = attributedict.get("decimal_digits", 2)
        interchangeable_with = attributedict.get("interchangeable_with")
        preferred_ticker = attributedict.get("preferred_ticker")

        attributedict["ticker"] = ticker.split(".")[-1] if ticker else ""
        attributedict["currency"] = attributedict["ticker"]
        attributedict["decimal_digits"] = decimal_digits
        attributedict["interchangeable_with"] = sorted(interchangeable_with) if interchangeable_with else None
        attributedict["preferred_ticker"] = preferred_ticker if preferred_ticker else None

        attributedict["_meta"] = bool(not bases)
        attributedict["as_string"] = lambda: str(attributedict["ticker"])
        attributedict["as_str"] = lambda: str(attributedict["ticker"])

        result: Type[BaseCurrency] = type.__new__(cls, name, bases, attributedict)
        return result

    def money(
        self,
        amount: Optional[Union["Money", Decimal, int, float, str, object]] = None,
        from_sub_units: Optional[bool] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        value: Optional[Union["Money", Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> "Money":
        kwargs.pop("currency", None)

        return Money(
            amount,
            currency=cast(BaseCurrency, self),
            from_sub_units=from_sub_units,
            units=units,
            nanos=nanos,
            value=value,
            currency_code=currency_code,
            **kwargs,
        )

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be deleted")

    def __repr__(self) -> str:
        if self._meta:
            return "<class 'stockholm.currency.Currency'>"
        return f'<stockholm.Currency: "{self}">'

    def __str__(self) -> str:
        if self._meta:
            return "<class 'stockholm.currency.Currency'>"
        return self.ticker or ""

    def __format__(self, format_spec: str) -> str:
        output = str(self)
        if format_spec.endswith("c"):
            format_spec = f"{format_spec[:-1]}s"
        return f"{output:{format_spec}}"

    def __eq__(self, other: Any) -> bool:
        if self.ticker:
            if not other:
                return False
            elif isinstance(other, BaseCurrency):
                return bool(self.ticker == other.ticker)
            elif isinstance(other, str):
                return bool(self.ticker == other)
        else:
            if isinstance(other, BaseCurrency):
                return not other.ticker
            elif isinstance(other, str):
                return bool(other == "")
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    @property  # type: ignore
    def __class__(self) -> Any:
        return BaseCurrency

    def __hash__(self) -> int:
        return hash(
            (
                "stockholm.MetaCurrency",
                self.ticker,
                self.decimal_digits,
                self.interchangeable_with,
                self.preferred_ticker,
            )
        )

    def __bool__(self) -> bool:
        return bool(self.ticker)


class BaseCurrency(metaclass=MetaCurrency):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]
    _meta: bool

    def __init__(
        self,
        currency: Optional[Union["Currency", str]] = None,
        decimal_digits: Optional[int] = None,
        interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]] = None,
        preferred_ticker: Optional[str] = None,
    ) -> None:
        if not self._meta:
            raise TypeError("'BaseCurrency' object is not callable")

        if currency and isinstance(currency, BaseCurrency):
            object.__setattr__(self, "ticker", currency.ticker)
            decimal_digits = currency.decimal_digits if decimal_digits is None else decimal_digits
            interchangeable_with = (
                currency.interchangeable_with if interchangeable_with is None else interchangeable_with
            )
            preferred_ticker = currency.preferred_ticker if preferred_ticker is None else preferred_ticker
        elif currency and isinstance(currency, str):
            object.__setattr__(self, "ticker", currency)
        else:
            object.__setattr__(self, "ticker", "")

        object.__setattr__(self, "currency", self.ticker)
        object.__setattr__(self, "decimal_digits", 2 if decimal_digits is None else decimal_digits)
        object.__setattr__(self, "interchangeable_with", sorted(interchangeable_with) if interchangeable_with else None)
        object.__setattr__(self, "preferred_ticker", preferred_ticker if preferred_ticker else None)

        object.__setattr__(self, "_meta", False)
        object.__setattr__(self, "as_string", lambda: str(self))
        object.__setattr__(self, "as_str", lambda: str(self))
        object.__setattr__(self, "money", lambda *args, **kwargs: self._money(*args, **kwargs))

    def _money(
        self,
        amount: Optional[Union["Money", Decimal, int, float, str, object]] = None,
        from_sub_units: Optional[bool] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        value: Optional[Union["Money", Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> "Money":
        kwargs.pop("currency", None)

        return Money(
            amount,
            currency=self,
            from_sub_units=from_sub_units,
            units=units,
            nanos=nanos,
            value=value,
            currency_code=currency_code,
            **kwargs,
        )

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be deleted")

    def __repr__(self) -> str:
        return f'<stockholm.Currency: "{self.ticker}">'

    def __str__(self) -> str:
        return self.ticker or ""

    def __format__(self, format_spec: str) -> str:
        output = str(self)
        if format_spec.endswith("c"):
            format_spec = f"{format_spec[:-1]}s"
        return f"{output:{format_spec}}"

    def __eq__(self, other: Any) -> bool:
        if self.ticker:
            if not other:
                return False
            elif isinstance(other, BaseCurrency):
                return bool(self.ticker == other.ticker)
            elif isinstance(other, str):
                return bool(self.ticker == other)
        else:
            if isinstance(other, BaseCurrency):
                return not other.ticker
            elif isinstance(other, str):
                return bool(other == "")
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(
            ("stockholm.Currency", self.ticker, self.decimal_digits, self.interchangeable_with, self.preferred_ticker)
        )

    def __bool__(self) -> bool:
        return bool(self.ticker)


# ISO 4217 currency codes
class AED(BaseCurrency):
    pass


class AFN(BaseCurrency):
    pass


class ALL(BaseCurrency):
    pass


class AMD(BaseCurrency):
    pass


class ANG(BaseCurrency):
    pass


class AOA(BaseCurrency):
    pass


class ARS(BaseCurrency):
    pass


class AUD(BaseCurrency):
    pass


class AWG(BaseCurrency):
    pass


class AZN(BaseCurrency):
    pass


class BAM(BaseCurrency):
    pass


class BBD(BaseCurrency):
    pass


class BDT(BaseCurrency):
    pass


class BGN(BaseCurrency):
    pass


class BHD(BaseCurrency):
    pass


class BIF(BaseCurrency):
    decimal_digits = 2


class BMD(BaseCurrency):
    pass


class BND(BaseCurrency):
    pass


class BOB(BaseCurrency):
    pass


class BOV(BaseCurrency):
    pass


class BRL(BaseCurrency):
    pass


class BSD(BaseCurrency):
    pass


class BTN(BaseCurrency):
    pass


class BWP(BaseCurrency):
    pass


class BYN(BaseCurrency):
    pass


class BZD(BaseCurrency):
    pass


class CAD(BaseCurrency):
    pass


class CDF(BaseCurrency):
    pass


class CHE(BaseCurrency):
    pass


class CHF(BaseCurrency):
    pass


class CHW(BaseCurrency):
    pass


class CLF(BaseCurrency):
    decimal_digits = 4


class CLP(BaseCurrency):
    decimal_digits = 0


class CNY(BaseCurrency):
    interchangeable_with = ("CNH", "RMB")


class COP(BaseCurrency):
    pass


class COU(BaseCurrency):
    pass


class CRC(BaseCurrency):
    pass


class CUC(BaseCurrency):
    pass


class CUP(BaseCurrency):
    pass


class CVE(BaseCurrency):
    pass


class CZK(BaseCurrency):
    pass


class DJF(BaseCurrency):
    decimal_digits = 0


class DKK(BaseCurrency):
    pass


class DOP(BaseCurrency):
    pass


class DZD(BaseCurrency):
    pass


class EGP(BaseCurrency):
    pass


class ERN(BaseCurrency):
    pass


class ETB(BaseCurrency):
    pass


class EUR(BaseCurrency):
    pass


class FJD(BaseCurrency):
    pass


class FKP(BaseCurrency):
    pass


class GBP(BaseCurrency):
    pass


class GEL(BaseCurrency):
    pass


class GHS(BaseCurrency):
    pass


class GIP(BaseCurrency):
    pass


class GMD(BaseCurrency):
    pass


class GNF(BaseCurrency):
    decimal_digits = 0


class GTQ(BaseCurrency):
    pass


class GYD(BaseCurrency):
    pass


class HKD(BaseCurrency):
    pass


class HNL(BaseCurrency):
    pass


class HRK(BaseCurrency):
    pass


class HTG(BaseCurrency):
    pass


class HUF(BaseCurrency):
    pass


class IDR(BaseCurrency):
    pass


class ILS(BaseCurrency):
    interchangeable_with = ("NIS",)


class INR(BaseCurrency):
    pass


class IQD(BaseCurrency):
    decimal_digits = 3


class IRR(BaseCurrency):
    pass


class ISK(BaseCurrency):
    decimal_digits = 0


class JMD(BaseCurrency):
    pass


class JOD(BaseCurrency):
    decimal_digits = 3


class JPY(BaseCurrency):
    decimal_digits = 0


class KES(BaseCurrency):
    pass


class KGS(BaseCurrency):
    pass


class KHR(BaseCurrency):
    pass


class KMF(BaseCurrency):
    decimal_digits = 0


class KPW(BaseCurrency):
    pass


class KRW(BaseCurrency):
    decimal_digits = 0


class KWD(BaseCurrency):
    decimal_digits = 3


class KYD(BaseCurrency):
    pass


class KZT(BaseCurrency):
    pass


class LAK(BaseCurrency):
    pass


class LBP(BaseCurrency):
    pass


class LKR(BaseCurrency):
    pass


class LRD(BaseCurrency):
    pass


class LSL(BaseCurrency):
    pass


class LYD(BaseCurrency):
    decimal_digits = 3


class MAD(BaseCurrency):
    pass


class MDL(BaseCurrency):
    pass


class MGA(BaseCurrency):
    pass


class MKD(BaseCurrency):
    pass


class MMK(BaseCurrency):
    pass


class MNT(BaseCurrency):
    pass


class MOP(BaseCurrency):
    pass


class MRU(BaseCurrency):
    pass


class MUR(BaseCurrency):
    pass


class MVR(BaseCurrency):
    pass


class MWK(BaseCurrency):
    pass


class MXN(BaseCurrency):
    pass


class MXV(BaseCurrency):
    pass


class MYR(BaseCurrency):
    pass


class MZN(BaseCurrency):
    pass


class NAD(BaseCurrency):
    pass


class NGN(BaseCurrency):
    pass


class NIO(BaseCurrency):
    pass


class NOK(BaseCurrency):
    pass


class NPR(BaseCurrency):
    pass


class NZD(BaseCurrency):
    pass


class OMR(BaseCurrency):
    decimal_digits = 3


class PAB(BaseCurrency):
    pass


class PEN(BaseCurrency):
    pass


class PGK(BaseCurrency):
    pass


class PHP(BaseCurrency):
    pass


class PKR(BaseCurrency):
    pass


class PLN(BaseCurrency):
    pass


class PYG(BaseCurrency):
    decimal_digits = 0


class QAR(BaseCurrency):
    pass


class RON(BaseCurrency):
    pass


class RSD(BaseCurrency):
    pass


class RUB(BaseCurrency):
    pass


class RWF(BaseCurrency):
    decimal_digits = 0


class SAR(BaseCurrency):
    pass


class SBD(BaseCurrency):
    pass


class SCR(BaseCurrency):
    pass


class SDG(BaseCurrency):
    pass


class SEK(BaseCurrency):
    pass


class SGD(BaseCurrency):
    pass


class SHP(BaseCurrency):
    pass


class SLL(BaseCurrency):
    pass


class SOS(BaseCurrency):
    pass


class SRD(BaseCurrency):
    pass


class SSP(BaseCurrency):
    pass


class STN(BaseCurrency):
    pass


class SVC(BaseCurrency):
    pass


class SYP(BaseCurrency):
    pass


class SZL(BaseCurrency):
    pass


class THB(BaseCurrency):
    pass


class TJS(BaseCurrency):
    pass


class TMT(BaseCurrency):
    pass


class TND(BaseCurrency):
    decimal_digits = 3


class TOP(BaseCurrency):
    pass


class TRY(BaseCurrency):
    pass


class TTD(BaseCurrency):
    pass


class TWD(BaseCurrency):
    interchangeable_with = ("NTD",)


class TZS(BaseCurrency):
    pass


class UAH(BaseCurrency):
    pass


class UGX(BaseCurrency):
    decimal_digits = 0


class USD(BaseCurrency):
    pass


class USN(BaseCurrency):
    pass


class UYI(BaseCurrency):
    decimal_digits = 0


class UYU(BaseCurrency):
    pass


class UYW(BaseCurrency):
    decimal_digits = 4


class UZS(BaseCurrency):
    pass


class VES(BaseCurrency):
    pass


class VND(BaseCurrency):
    decimal_digits = 0


class VUV(BaseCurrency):
    decimal_digits = 0


class WST(BaseCurrency):
    pass


class XAF(BaseCurrency):
    decimal_digits = 0


class XAG(BaseCurrency):
    pass


class XAU(BaseCurrency):
    pass


class XBA(BaseCurrency):
    pass


class XBB(BaseCurrency):
    pass


class XBC(BaseCurrency):
    pass


class XBD(BaseCurrency):
    pass


class XCD(BaseCurrency):
    pass


class XDR(BaseCurrency):
    pass


class XOF(BaseCurrency):
    decimal_digits = 0


class XPD(BaseCurrency):
    pass


class XPF(BaseCurrency):
    decimal_digits = 0


class XPT(BaseCurrency):
    pass


class XSU(BaseCurrency):
    pass


class XTS(BaseCurrency):
    pass


class XUA(BaseCurrency):
    pass


class XXX(BaseCurrency):
    pass


class YER(BaseCurrency):
    pass


class ZAR(BaseCurrency):
    pass


class ZMW(BaseCurrency):
    pass


class ZWL(BaseCurrency):
    pass


# Unofficial currency codes


class CNH(BaseCurrency):
    interchangeable_with = ("CNY", "RMB")
    preferred_ticker = "CNY"


class GGP(BaseCurrency):
    pass


class IMP(BaseCurrency):
    pass


class JED(BaseCurrency):
    pass


class KID(BaseCurrency):
    pass


class NIS(BaseCurrency):
    interchangeable_with = ("ILS",)
    preferred_ticker = "ILS"


class NTD(BaseCurrency):
    interchangeable_with = ("TWD",)
    preferred_ticker = "TWD"


class PRB(BaseCurrency):
    pass


class SLS(BaseCurrency):
    pass


class RMB(BaseCurrency):
    interchangeable_with = ("CNH", "RMB")
    preferred_ticker = "CNY"


class TVD(BaseCurrency):
    pass


class ZWB(BaseCurrency):
    pass


# Historical currency codes


class ADF(BaseCurrency):
    pass


class ADP(BaseCurrency):
    decimal_digits = 0


class AFA(BaseCurrency):
    pass


class AOK(BaseCurrency):
    decimal_digits = 0


class AON(BaseCurrency):
    decimal_digits = 0


class AOR(BaseCurrency):
    decimal_digits = 0


class ARL(BaseCurrency):
    pass


class ARP(BaseCurrency):
    pass


class ARA(BaseCurrency):
    pass


class ATS(BaseCurrency):
    pass


class AZM(BaseCurrency):
    decimal_digits = 0


class BAD(BaseCurrency):
    pass


class BEF(BaseCurrency):
    pass


class BGL(BaseCurrency):
    pass


class BOP(BaseCurrency):
    pass


class BRB(BaseCurrency):
    pass


class BRC(BaseCurrency):
    pass


class BRN(BaseCurrency):
    pass


class BRE(BaseCurrency):
    pass


class BRR(BaseCurrency):
    pass


class BYB(BaseCurrency):
    pass


class BYR(BaseCurrency):
    decimal_digits = 0


class CSD(BaseCurrency):
    pass


class CSK(BaseCurrency):
    pass


class CYP(BaseCurrency):
    pass


class DDM(BaseCurrency):
    pass


class DEM(BaseCurrency):
    pass


class ECS(BaseCurrency):
    decimal_digits = 0


class ECV(BaseCurrency):
    pass


class EEK(BaseCurrency):
    pass


class ESA(BaseCurrency):
    pass


class ESB(BaseCurrency):
    pass


class ESP(BaseCurrency):
    decimal_digits = 0


class FIM(BaseCurrency):
    pass


class FRF(BaseCurrency):
    pass


class GNE(BaseCurrency):
    pass


class GHC(BaseCurrency):
    decimal_digits = 0


class GQE(BaseCurrency):
    pass


class GRD(BaseCurrency):
    pass


class GWP(BaseCurrency):
    pass


class HRD(BaseCurrency):
    pass


class IEP(BaseCurrency):
    pass


class ILP(BaseCurrency):
    decimal_digits = 3


class ILR(BaseCurrency):
    pass


class ISJ(BaseCurrency):
    pass


class ITL(BaseCurrency):
    decimal_digits = 0


class LAJ(BaseCurrency):
    pass


class LTL(BaseCurrency):
    pass


class LUF(BaseCurrency):
    pass


class LVL(BaseCurrency):
    pass


class MAF(BaseCurrency):
    pass


class MCF(BaseCurrency):
    pass


class MGF(BaseCurrency):
    pass


class MKN(BaseCurrency):
    pass


class MLF(BaseCurrency):
    pass


class MVQ(BaseCurrency):
    pass


class MRO(BaseCurrency):
    pass


class MXP(BaseCurrency):
    pass


class MZM(BaseCurrency):
    decimal_digits = 0


class MTL(BaseCurrency):
    pass


class NIC(BaseCurrency):
    pass


class NLG(BaseCurrency):
    pass


class PEH(BaseCurrency):
    pass


class PEI(BaseCurrency):
    pass


class PLZ(BaseCurrency):
    pass


class PTE(BaseCurrency):
    decimal_digits = 0


class ROL(BaseCurrency):
    pass


class RUR(BaseCurrency):
    pass


class SDD(BaseCurrency):
    decimal_digits = 0


class SDP(BaseCurrency):
    pass


class SIT(BaseCurrency):
    pass


class SKK(BaseCurrency):
    pass


class SML(BaseCurrency):
    decimal_digits = 0


class SRG(BaseCurrency):
    pass


class STD(BaseCurrency):
    pass


class SUR(BaseCurrency):
    pass


class TJR(BaseCurrency):
    pass


class TMM(BaseCurrency):
    decimal_digits = 0


class TPE(BaseCurrency):
    pass


class TRL(BaseCurrency):
    decimal_digits = 0


class UAK(BaseCurrency):
    pass


class UGS(BaseCurrency):
    pass


class USS(BaseCurrency):
    pass


class UYP(BaseCurrency):
    pass


class UYN(BaseCurrency):
    pass


class VAL(BaseCurrency):
    decimal_digits = 0


class VEB(BaseCurrency):
    pass


class VEF(BaseCurrency):
    pass


class XEU(BaseCurrency):
    pass


class XFO(BaseCurrency):
    pass


class XFU(BaseCurrency):
    pass


class YDD(BaseCurrency):
    pass


class YUD(BaseCurrency):
    pass


class YUN(BaseCurrency):
    pass


class YUR(BaseCurrency):
    pass


class YUO(BaseCurrency):
    pass


class YUG(BaseCurrency):
    pass


class YUM(BaseCurrency):
    pass


class ZAL(BaseCurrency):
    pass


class ZMK(BaseCurrency):
    pass


class ZRZ(BaseCurrency):
    decimal_digits = 3


class ZRN(BaseCurrency):
    pass


class ZWC(BaseCurrency):
    pass


class ZWD(BaseCurrency):
    pass


class ZWN(BaseCurrency):
    pass


class ZWR(BaseCurrency):
    pass


# Cryptocurrencies


class Bitcoin(BaseCurrency):
    ticker = "BTC"


BTC = Bitcoin
XBT = Bitcoin


class Ethereum(BaseCurrency):
    ticker = "ETH"


ETH = Ethereum


class XRP(BaseCurrency):
    ticker = "XRP"


class Tether(BaseCurrency):
    ticker = "USDT"


USDT = Tether


class USDCoin(BaseCurrency):
    ticker = "USDC"


CoinbaseUSDC = USDCoin
USDC = USDCoin


class BitcoinCash(BaseCurrency):
    ticker = "BCH"


BCH = BitcoinCash
XCH = BitcoinCash


class LiteCoin(BaseCurrency):
    ticker = "LTC"


LTC = LiteCoin


class EOS(BaseCurrency):
    ticker = "EOS"


class BinanceCoin(BaseCurrency):
    ticker = "BNB"


BNB = BinanceCoin


class StellarLumen(BaseCurrency):
    ticker = "XLM"


XLM = StellarLumen


class Monero(BaseCurrency):
    ticker = "XMR"


XMR = Monero


class DogeCoin(BaseCurrency):
    ticker = "DOGE"


DOGE = DogeCoin


def get_currency(ticker: str) -> BaseCurrency:
    return cast(BaseCurrency, getattr(sys.modules[__name__], ticker, BaseCurrency(ticker)))


def all_currencies() -> List[str]:
    return [ticker for ticker in dir(sys.modules[__name__]) if ticker and ticker == ticker.upper()]


class Currency(type):
    def __new__(cls, *args: Any, **kwargs: Any) -> BaseCurrency:  # type: ignore
        result: BaseCurrency = BaseCurrency(*args, **kwargs)
        return result

    @staticmethod
    def _load_currencies(currencies: List[str]) -> None:
        for ticker in currencies:
            setattr(Currency, ticker, getattr(sys.modules[__name__], ticker))


Currency._load_currencies(all_currencies())

from stockholm.money import Money  # noqa isort:skip
