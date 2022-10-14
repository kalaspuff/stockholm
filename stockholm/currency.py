from __future__ import annotations

import sys
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union, cast


class DefaultCurrencyValue(type):
    pass


class DefaultCurrency(metaclass=DefaultCurrencyValue):
    def __new__(cls: Type[DefaultCurrency]) -> DefaultCurrency:
        raise TypeError("'DefaultCurrency' object is not callable")


class MetaCurrency(type):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]
    _meta: bool

    def __new__(cls: Type[MetaCurrency], name: str, bases: Tuple[type, ...], attributedict: Dict) -> MetaCurrency:
        ticker = attributedict.get("ticker", attributedict.get("__qualname__"))
        decimal_digits = attributedict.get("decimal_digits", 2)
        interchangeable_with = attributedict.get("interchangeable_with")
        preferred_ticker = attributedict.get("preferred_ticker")

        attributedict["ticker"] = ticker.split(".")[-1] if ticker else ""
        attributedict["currency"] = attributedict["ticker"]
        attributedict["decimal_digits"] = decimal_digits
        attributedict["interchangeable_with"] = tuple(sorted(interchangeable_with)) if interchangeable_with else None
        attributedict["preferred_ticker"] = preferred_ticker if preferred_ticker else None

        attributedict["_meta"] = bool(
            not bases
            or (
                name in ("BaseCurrency", "Currency")
                and len(bases) == 1
                and str(type(bases[0])) == "<class 'stockholm.currency.MetaCurrency'>"
            )
        )
        attributedict["as_string"] = lambda: str(attributedict["ticker"])
        attributedict["as_str"] = lambda: str(attributedict["ticker"])

        return cast(Type["BaseCurrency"], super().__new__(cls, name, bases, attributedict))

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

    def __instancecheck__(self, instance: Any) -> bool:
        return_value = super().__instancecheck__(instance)
        if not return_value and type(instance) is BaseCurrencyType:
            return True
        return return_value


class BaseCurrencyType(metaclass=MetaCurrency):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]
    _meta: bool

    def __init__(
        self,
        currency: Optional[Union[CurrencyValue, str]] = None,
        decimal_digits: Optional[int] = None,
        interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]] = None,
        preferred_ticker: Optional[str] = None,
    ) -> None:
        if currency and isinstance(currency, BaseCurrency):
            object.__setattr__(self, "ticker", currency.ticker)
            decimal_digits = currency.decimal_digits if decimal_digits is None else decimal_digits
            interchangeable_with = (
                currency.interchangeable_with if interchangeable_with is None else tuple(interchangeable_with)
            )
            preferred_ticker = currency.preferred_ticker if preferred_ticker is None else preferred_ticker
        elif currency and isinstance(currency, str):
            object.__setattr__(self, "ticker", currency)
        else:
            object.__setattr__(self, "ticker", "")

        object.__setattr__(self, "currency", self.ticker)
        object.__setattr__(self, "decimal_digits", 2 if decimal_digits is None else decimal_digits)
        object.__setattr__(
            self, "interchangeable_with", tuple(sorted(interchangeable_with)) if interchangeable_with else None
        )
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


class BaseCurrency(BaseCurrencyType):
    def __new__(
        cls,
        currency: Optional[Union[CurrencyValue, str]] = None,
        decimal_digits: Optional[int] = None,
        interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]] = None,
        preferred_ticker: Optional[str] = None,
    ) -> BaseCurrency:
        if not cls._meta:
            raise TypeError("'BaseCurrency' object is not callable")
        return cast(
            BaseCurrency,
            BaseCurrencyType(
                currency=currency,
                decimal_digits=decimal_digits,
                interchangeable_with=interchangeable_with,
                preferred_ticker=preferred_ticker,
            ),
        )


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


# Note to future self – this is generally bad practice (but helps with type hint annotations).
class Currency(BaseCurrency):
    ADF = ADF
    ADP = ADP
    AED = AED
    AFA = AFA
    AFN = AFN
    ALL = ALL
    AMD = AMD
    ANG = ANG
    AOA = AOA
    AOK = AOK
    AON = AON
    AOR = AOR
    ARA = ARA
    ARL = ARL
    ARP = ARP
    ARS = ARS
    ATS = ATS
    AUD = AUD
    AWG = AWG
    AZM = AZM
    AZN = AZN
    BAD = BAD
    BAM = BAM
    BBD = BBD
    BCH = BCH
    BDT = BDT
    BEF = BEF
    BGL = BGL
    BGN = BGN
    BHD = BHD
    BIF = BIF
    BMD = BMD
    BNB = BNB
    BND = BND
    BOB = BOB
    BOP = BOP
    BOV = BOV
    BRB = BRB
    BRC = BRC
    BRE = BRE
    BRL = BRL
    BRN = BRN
    BRR = BRR
    BSD = BSD
    BTC = BTC
    BTN = BTN
    BWP = BWP
    BYB = BYB
    BYN = BYN
    BYR = BYR
    BZD = BZD
    CAD = CAD
    CDF = CDF
    CHE = CHE
    CHF = CHF
    CHW = CHW
    CLF = CLF
    CLP = CLP
    CNH = CNH
    CNY = CNY
    COP = COP
    COU = COU
    CRC = CRC
    CSD = CSD
    CSK = CSK
    CUC = CUC
    CUP = CUP
    CVE = CVE
    CYP = CYP
    CZK = CZK
    DDM = DDM
    DEM = DEM
    DJF = DJF
    DKK = DKK
    DOGE = DOGE
    DOP = DOP
    DZD = DZD
    ECS = ECS
    ECV = ECV
    EEK = EEK
    EGP = EGP
    EOS = EOS
    ERN = ERN
    ESA = ESA
    ESB = ESB
    ESP = ESP
    ETB = ETB
    ETH = ETH
    EUR = EUR
    FIM = FIM
    FJD = FJD
    FKP = FKP
    FRF = FRF
    GBP = GBP
    GEL = GEL
    GGP = GGP
    GHC = GHC
    GHS = GHS
    GIP = GIP
    GMD = GMD
    GNE = GNE
    GNF = GNF
    GQE = GQE
    GRD = GRD
    GTQ = GTQ
    GWP = GWP
    GYD = GYD
    HKD = HKD
    HNL = HNL
    HRD = HRD
    HRK = HRK
    HTG = HTG
    HUF = HUF
    IDR = IDR
    IEP = IEP
    ILP = ILP
    ILR = ILR
    ILS = ILS
    IMP = IMP
    INR = INR
    IQD = IQD
    IRR = IRR
    ISJ = ISJ
    ISK = ISK
    ITL = ITL
    JED = JED
    JMD = JMD
    JOD = JOD
    JPY = JPY
    KES = KES
    KGS = KGS
    KHR = KHR
    KID = KID
    KMF = KMF
    KPW = KPW
    KRW = KRW
    KWD = KWD
    KYD = KYD
    KZT = KZT
    LAJ = LAJ
    LAK = LAK
    LBP = LBP
    LKR = LKR
    LRD = LRD
    LSL = LSL
    LTC = LTC
    LTL = LTL
    LUF = LUF
    LVL = LVL
    LYD = LYD
    MAD = MAD
    MAF = MAF
    MCF = MCF
    MDL = MDL
    MGA = MGA
    MGF = MGF
    MKD = MKD
    MKN = MKN
    MLF = MLF
    MMK = MMK
    MNT = MNT
    MOP = MOP
    MRO = MRO
    MRU = MRU
    MTL = MTL
    MUR = MUR
    MVQ = MVQ
    MVR = MVR
    MWK = MWK
    MXN = MXN
    MXP = MXP
    MXV = MXV
    MYR = MYR
    MZM = MZM
    MZN = MZN
    NAD = NAD
    NGN = NGN
    NIC = NIC
    NIO = NIO
    NIS = NIS
    NLG = NLG
    NOK = NOK
    NPR = NPR
    NTD = NTD
    NZD = NZD
    OMR = OMR
    PAB = PAB
    PEH = PEH
    PEI = PEI
    PEN = PEN
    PGK = PGK
    PHP = PHP
    PKR = PKR
    PLN = PLN
    PLZ = PLZ
    PRB = PRB
    PTE = PTE
    PYG = PYG
    QAR = QAR
    RMB = RMB
    ROL = ROL
    RON = RON
    RSD = RSD
    RUB = RUB
    RUR = RUR
    RWF = RWF
    SAR = SAR
    SBD = SBD
    SCR = SCR
    SDD = SDD
    SDG = SDG
    SDP = SDP
    SEK = SEK
    SGD = SGD
    SHP = SHP
    SIT = SIT
    SKK = SKK
    SLL = SLL
    SLS = SLS
    SML = SML
    SOS = SOS
    SRD = SRD
    SRG = SRG
    SSP = SSP
    STD = STD
    STN = STN
    SUR = SUR
    SVC = SVC
    SYP = SYP
    SZL = SZL
    THB = THB
    TJR = TJR
    TJS = TJS
    TMM = TMM
    TMT = TMT
    TND = TND
    TOP = TOP
    TPE = TPE
    TRL = TRL
    TRY = TRY
    TTD = TTD
    TVD = TVD
    TWD = TWD
    TZS = TZS
    UAH = UAH
    UAK = UAK
    UGS = UGS
    UGX = UGX
    USD = USD
    USDC = USDC
    USDT = USDT
    USN = USN
    USS = USS
    UYI = UYI
    UYN = UYN
    UYP = UYP
    UYU = UYU
    UYW = UYW
    UZS = UZS
    VAL = VAL
    VEB = VEB
    VEF = VEF
    VES = VES
    VND = VND
    VUV = VUV
    WST = WST
    XAF = XAF
    XAG = XAG
    XAU = XAU
    XBA = XBA
    XBB = XBB
    XBC = XBC
    XBD = XBD
    XBT = XBT
    XCD = XCD
    XCH = XCH
    XDR = XDR
    XEU = XEU
    XFO = XFO
    XFU = XFU
    XLM = XLM
    XMR = XMR
    XOF = XOF
    XPD = XPD
    XPF = XPF
    XPT = XPT
    XRP = XRP
    XSU = XSU
    XTS = XTS
    XUA = XUA
    XXX = XXX
    YDD = YDD
    YER = YER
    YUD = YUD
    YUG = YUG
    YUM = YUM
    YUN = YUN
    YUO = YUO
    YUR = YUR
    ZAL = ZAL
    ZAR = ZAR
    ZMK = ZMK
    ZMW = ZMW
    ZRN = ZRN
    ZRZ = ZRZ
    ZWB = ZWB
    ZWC = ZWC
    ZWD = ZWD
    ZWL = ZWL
    ZWN = ZWN
    ZWR = ZWR


from .compat import CurrencyValue  # noqa isort:skip
from stockholm.money import Money  # noqa isort:skip
