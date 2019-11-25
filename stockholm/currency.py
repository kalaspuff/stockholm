from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union


class MetaCurrency(type):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]

    def __new__(cls, name: str, bases: Tuple[type, ...], attributedict: Dict) -> "MetaCurrency":
        ticker = attributedict.get("ticker", attributedict.get("__qualname__"))
        decimal_digits = attributedict.get("decimal_digits", 2)
        interchangeable_with = attributedict.get("interchangeable_with")
        preferred_ticker = attributedict.get("preferred_ticker")

        attributedict["ticker"] = ticker.split(".")[-1] if ticker else ""
        attributedict["currency"] = attributedict["ticker"]
        attributedict["decimal_digits"] = decimal_digits
        attributedict["interchangeable_with"] = interchangeable_with
        attributedict["preferred_ticker"] = preferred_ticker

        result: Type[Currency] = type.__new__(cls, name, bases, attributedict)
        return result

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be deleted")

    def __repr__(self) -> str:
        return f'<stockholm.Currency: "{self}">'

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
            elif isinstance(other, Currency):
                return bool(self.ticker == other.ticker)
            elif isinstance(other, str):
                return bool(self.ticker == other)
        else:
            if isinstance(other, Currency):
                return not other.ticker
            elif isinstance(other, str):
                return bool(other == "")
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    @property  # type: ignore
    def __class__(self) -> Any:
        return Currency

    def __hash__(self) -> int:
        return hash(("stockholm.MetaCurrency", self.ticker))

    def __bool__(self) -> bool:
        return bool(self.ticker)


class Currency(metaclass=MetaCurrency):
    ticker: str
    decimal_digits: int
    interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
    preferred_ticker: Optional[str]

    def __init__(
        self,
        currency: Optional[Union["Currency", str]] = None,
        decimal_digits: Optional[int] = None,
        interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]] = None,
        preferred_ticker: Optional[str] = None,
    ) -> None:
        if currency and isinstance(currency, Currency):
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
        object.__setattr__(self, "interchangeable_with", interchangeable_with)
        object.__setattr__(self, "preferred_ticker", preferred_ticker)

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
            elif isinstance(other, Currency):
                return bool(self.ticker == other.ticker)
            elif isinstance(other, str):
                return bool(self.ticker == other)
        else:
            if isinstance(other, Currency):
                return not other.ticker
            elif isinstance(other, str):
                return bool(other == "")
        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(("stockholm.Currency", self.ticker))

    def __bool__(self) -> bool:
        return bool(self.ticker)


# ISO 4217 currency codes
class AED(Currency):
    pass


class AFN(Currency):
    pass


class ALL(Currency):
    pass


class AMD(Currency):
    pass


class ANG(Currency):
    pass


class AOA(Currency):
    pass


class ARS(Currency):
    pass


class AUD(Currency):
    pass


class AWG(Currency):
    pass


class AZN(Currency):
    pass


class BAM(Currency):
    pass


class BBD(Currency):
    pass


class BDT(Currency):
    pass


class BGN(Currency):
    pass


class BHD(Currency):
    pass


class BIF(Currency):
    decimal_digits = 2


class BMD(Currency):
    pass


class BND(Currency):
    pass


class BOB(Currency):
    pass


class BOV(Currency):
    pass


class BRL(Currency):
    pass


class BSD(Currency):
    pass


class BTN(Currency):
    pass


class BWP(Currency):
    pass


class BYN(Currency):
    pass


class BZD(Currency):
    pass


class CAD(Currency):
    pass


class CDF(Currency):
    pass


class CHE(Currency):
    pass


class CHF(Currency):
    pass


class CHW(Currency):
    pass


class CLF(Currency):
    decimal_digits = 4


class CLP(Currency):
    decimal_digits = 0


class CNY(Currency):
    interchangeable_with = ("CNH", "RMB")


class COP(Currency):
    pass


class COU(Currency):
    pass


class CRC(Currency):
    pass


class CUC(Currency):
    pass


class CUP(Currency):
    pass


class CVE(Currency):
    pass


class CZK(Currency):
    pass


class DJF(Currency):
    decimal_digits = 0


class DKK(Currency):
    pass


class DOP(Currency):
    pass


class DZD(Currency):
    pass


class EGP(Currency):
    pass


class ERN(Currency):
    pass


class ETB(Currency):
    pass


class EUR(Currency):
    pass


class FJD(Currency):
    pass


class FKP(Currency):
    pass


class GBP(Currency):
    pass


class GEL(Currency):
    pass


class GHS(Currency):
    pass


class GIP(Currency):
    pass


class GMD(Currency):
    pass


class GNF(Currency):
    decimal_digits = 0


class GTQ(Currency):
    pass


class GYD(Currency):
    pass


class HKD(Currency):
    pass


class HNL(Currency):
    pass


class HRK(Currency):
    pass


class HTG(Currency):
    pass


class HUF(Currency):
    pass


class IDR(Currency):
    pass


class ILS(Currency):
    interchangeable_with = ("NIS",)


class INR(Currency):
    pass


class IQD(Currency):
    decimal_digits = 3


class IRR(Currency):
    pass


class ISK(Currency):
    decimal_digits = 0


class JMD(Currency):
    pass


class JOD(Currency):
    decimal_digits = 3


class JPY(Currency):
    decimal_digits = 0


class KES(Currency):
    pass


class KGS(Currency):
    pass


class KHR(Currency):
    pass


class KMF(Currency):
    decimal_digits = 0


class KPW(Currency):
    pass


class KRW(Currency):
    decimal_digits = 0


class KWD(Currency):
    decimal_digits = 3


class KYD(Currency):
    pass


class KZT(Currency):
    pass


class LAK(Currency):
    pass


class LBP(Currency):
    pass


class LKR(Currency):
    pass


class LRD(Currency):
    pass


class LSL(Currency):
    pass


class LYD(Currency):
    decimal_digits = 3


class MAD(Currency):
    pass


class MDL(Currency):
    pass


class MGA(Currency):
    pass


class MKD(Currency):
    pass


class MMK(Currency):
    pass


class MNT(Currency):
    pass


class MOP(Currency):
    pass


class MRU(Currency):
    pass


class MUR(Currency):
    pass


class MVR(Currency):
    pass


class MWK(Currency):
    pass


class MXN(Currency):
    pass


class MXV(Currency):
    pass


class MYR(Currency):
    pass


class MZN(Currency):
    pass


class NAD(Currency):
    pass


class NGN(Currency):
    pass


class NIO(Currency):
    pass


class NOK(Currency):
    pass


class NPR(Currency):
    pass


class NZD(Currency):
    pass


class OMR(Currency):
    decimal_digits = 3


class PAB(Currency):
    pass


class PEN(Currency):
    pass


class PGK(Currency):
    pass


class PHP(Currency):
    pass


class PKR(Currency):
    pass


class PLN(Currency):
    pass


class PYG(Currency):
    decimal_digits = 0


class QAR(Currency):
    pass


class RON(Currency):
    pass


class RSD(Currency):
    pass


class RUB(Currency):
    pass


class RWF(Currency):
    decimal_digits = 0


class SAR(Currency):
    pass


class SBD(Currency):
    pass


class SCR(Currency):
    pass


class SDG(Currency):
    pass


class SEK(Currency):
    pass


class SGD(Currency):
    pass


class SHP(Currency):
    pass


class SLL(Currency):
    pass


class SOS(Currency):
    pass


class SRD(Currency):
    pass


class SSP(Currency):
    pass


class STN(Currency):
    pass


class SVC(Currency):
    pass


class SYP(Currency):
    pass


class SZL(Currency):
    pass


class THB(Currency):
    pass


class TJS(Currency):
    pass


class TMT(Currency):
    pass


class TND(Currency):
    decimal_digits = 3


class TOP(Currency):
    pass


class TRY(Currency):
    pass


class TTD(Currency):
    pass


class TWD(Currency):
    interchangeable_with = ("NTD",)


class TZS(Currency):
    pass


class UAH(Currency):
    pass


class UGX(Currency):
    decimal_digit = 0


class USD(Currency):
    pass


class USN(Currency):
    pass


class UYI(Currency):
    decimal_digits = 0


class UYU(Currency):
    pass


class UYW(Currency):
    decimal_digits = 4


class UZS(Currency):
    pass


class VES(Currency):
    pass


class VND(Currency):
    decimal_digits = 0


class VUV(Currency):
    decimal_digits = 0


class WST(Currency):
    pass


class XAF(Currency):
    decimal_digits = 0


class XAG(Currency):
    pass


class XAU(Currency):
    pass


class XBA(Currency):
    pass


class XBB(Currency):
    pass


class XBC(Currency):
    pass


class XBD(Currency):
    pass


class XCD(Currency):
    pass


class XDR(Currency):
    pass


class XOF(Currency):
    decimal_digits = 0


class XPD(Currency):
    pass


class XPF(Currency):
    decimal_digits = 0


class XPT(Currency):
    pass


class XSU(Currency):
    pass


class XTS(Currency):
    pass


class XUA(Currency):
    pass


class XXX(Currency):
    pass


class YER(Currency):
    pass


class ZAR(Currency):
    pass


class ZMW(Currency):
    pass


class ZWL(Currency):
    pass


# Unofficial currency codes


class CNH(Currency):
    interchangeable_with = ("CNY", "RMB")
    preferred_ticker = "CNY"


class GGP(Currency):
    pass


class IMP(Currency):
    pass


class JED(Currency):
    pass


class KID(Currency):
    pass


class NIS(Currency):
    interchangeable_with = ("ILS",)
    preferred_ticker = "ILS"


class NTD(Currency):
    interchangeable_with = ("TWD",)
    preferred_ticker = "TWD"


class PRB(Currency):
    pass


class SLS(Currency):
    pass


class RMB(Currency):
    interchangeable_with = ("CNH", "RMB")
    preferred_ticker = "CNY"


class TVD(Currency):
    pass


class ZWB(Currency):
    pass


# Historical currency codes


class ADF(Currency):
    pass


class ADP(Currency):
    decimal_digits = 0


class AFA(Currency):
    pass


class AOK(Currency):
    decimal_digits = 0


class AON(Currency):
    decimal_digits = 0


class AOR(Currency):
    decimal_digits = 0


class ARL(Currency):
    pass


class ARP(Currency):
    pass


class ARA(Currency):
    pass


class ATS(Currency):
    pass


class AZM(Currency):
    decimal_digits = 0


class BAD(Currency):
    pass


class BEF(Currency):
    pass


class BGL(Currency):
    pass


class BOP(Currency):
    pass


class BRB(Currency):
    pass


class BRC(Currency):
    pass


class BRN(Currency):
    pass


class BRE(Currency):
    pass


class BRR(Currency):
    pass


class BYB(Currency):
    pass


class BYR(Currency):
    decimal_digits = 0


class CSD(Currency):
    pass


class CSK(Currency):
    pass


class CYP(Currency):
    pass


class DDM(Currency):
    pass


class DEM(Currency):
    pass


class ECS(Currency):
    decimal_digits = 0


class ECV(Currency):
    pass


class EEK(Currency):
    pass


class ESA(Currency):
    pass


class ESB(Currency):
    pass


class ESP(Currency):
    decimal_digits = 0


class FIM(Currency):
    pass


class FRF(Currency):
    pass


class GNE(Currency):
    pass


class GHC(Currency):
    decimal_digits = 0


class GQE(Currency):
    pass


class GRD(Currency):
    pass


class GWP(Currency):
    pass


class HRD(Currency):
    pass


class IEP(Currency):
    pass


class ILP(Currency):
    decimal_digits = 3


class ILR(Currency):
    pass


class ISJ(Currency):
    pass


class ITL(Currency):
    decimal_digits = 0


class LAJ(Currency):
    pass


class LTL(Currency):
    pass


class LUF(Currency):
    pass


class LVL(Currency):
    pass


class MAF(Currency):
    pass


class MCF(Currency):
    pass


class MGF(Currency):
    pass


class MKN(Currency):
    pass


class MLF(Currency):
    pass


class MVQ(Currency):
    pass


class MRO(Currency):
    pass


class MXP(Currency):
    pass


class MZM(Currency):
    decimal_digits = 0


class MTL(Currency):
    pass


class NIC(Currency):
    pass


class NLG(Currency):
    pass


class PEH(Currency):
    pass


class PEI(Currency):
    pass


class PLZ(Currency):
    pass


class PTE(Currency):
    decimal_digits = 0


class ROL(Currency):
    pass


class RUR(Currency):
    pass


class SDD(Currency):
    decimal_digits = 0


class SDP(Currency):
    pass


class SIT(Currency):
    pass


class SKK(Currency):
    pass


class SML(Currency):
    decimal_digits = 0


class SRG(Currency):
    pass


class STD(Currency):
    pass


class SUR(Currency):
    pass


class TJR(Currency):
    pass


class TMM(Currency):
    decimal_digits = 0


class TPE(Currency):
    pass


class TRL(Currency):
    decimal_digits = 0


class UAK(Currency):
    pass


class UGS(Currency):
    pass


class USS(Currency):
    pass


class UYP(Currency):
    pass


class UYN(Currency):
    pass


class VAL(Currency):
    decimal_digits = 0


class VEB(Currency):
    pass


class VEF(Currency):
    pass


class XEU(Currency):
    pass


class XFO(Currency):
    pass


class XFU(Currency):
    pass


class YDD(Currency):
    pass


class YUD(Currency):
    pass


class YUN(Currency):
    pass


class YUR(Currency):
    pass


class YUO(Currency):
    pass


class YUG(Currency):
    pass


class YUM(Currency):
    pass


class ZAL(Currency):
    pass


class ZMK(Currency):
    pass


class ZRZ(Currency):
    decimal_digits = 3


class ZRN(Currency):
    pass


class ZWC(Currency):
    pass


class ZWD(Currency):
    pass


class ZWN(Currency):
    pass


class ZWR(Currency):
    pass


# Cryptocurrencies


class Bitcoin(Currency):
    ticker = "BTC"


BTC = Bitcoin
XBT = Bitcoin


class Ethereum(Currency):
    ticker = "ETH"


ETH = Ethereum


class XRP(Currency):
    ticker = "XRP"


class Tether(Currency):
    ticker = "USDT"


USDT = Tether


class USDCoin(Currency):
    ticker = "USDC"


CoinbaseUSDC = USDCoin
USDC = USDCoin


class BitcoinCash(Currency):
    ticker = "BCH"


BCH = BitcoinCash
XCH = BitcoinCash


class LiteCoin(Currency):
    ticker = "LTC"


LTC = LiteCoin


class EOS(Currency):
    ticker = "EOS"


class BinanceCoin(Currency):
    ticker = "BNB"


BNB = BinanceCoin


class StellarLumen(Currency):
    ticker = "XLM"


XLM = StellarLumen


class Monero(Currency):
    ticker = "XMR"


XMR = Monero


class DogeCoin(Currency):
    ticker = "DOGE"


DOGE = DogeCoin
