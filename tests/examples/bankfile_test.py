from typing import List

from stockholm import Money, get_currency
from stockholm.exceptions import CurrencyMismatchError

example_content = """
000000000000001     388461894717 OLDSCHOOLFINTECHSOLUTIONS004711000003
471846827769   9173689 9999000192000000272947     USD  - 3336282671946
471846827769 557274901    1000824618000272944     USD  020000047284999
484761849926   4444205   37000116301000072944     USD  - 3336282671947
990000000000001X00000399300001132919USD                            END
"""


def get_transaction_amounts(content: str) -> List[Money]:
    amounts: List[Money] = []
    total_amount: Money = Money(0)
    transaction_count: int = 0
    transaction_count_validation: int = 0

    for line_num, line in enumerate(content.split("\n"), 1):
        if not line.strip():
            continue

        try:
            if line.startswith("00"):
                transaction_count = int(line[64:(64 + 6)])
            elif line.startswith("99"):
                total_amount = Money(line[25:(25 + 11)], from_sub_units=True, currency=get_currency(line[36:(36 + 3)]))
                transaction_count_validation = int(line[16:(16 + 6)])
                break
            elif line.startswith("4"):
                amount = Money(line[27:(27 + 9)], from_sub_units=True, currency=get_currency(line[50:(50 + 3)]))
                amounts.append((amount))
        except Exception as exc:
            raise Exception(f"Invalid content format – [line number = {line_num}, line length = {len(line)}, exception = ({type(exc)} – '{exc}')]")

    if transaction_count != transaction_count_validation:
        raise Exception(f"Transaction count does not match – ['00': count = {transaction_count} | '99': count = {transaction_count_validation}]")

    if transaction_count != len(amounts):
        raise Exception(f"Transaction count does not match – ['00': count = {transaction_count} | '4X': count = {len(amounts)}]")

    if not transaction_count:
        return amounts

    total_amount_sum: Money = Money(0)
    try:
        total_amount_sum = Money.sum(amounts)
    except CurrencyMismatchError:
        currency_codes_string = "', '".join({str(a.currency_code) for a in amounts})
        raise Exception(f"Multiple currency codes within the same content block – ['00': currency = '{total_amount.currency}' | '4X': currencies = ('{currency_codes_string}')]")

    if total_amount.currency != total_amount_sum.currency:
        raise Exception(f"Currency codes does not match – ['00': currency = '{total_amount.currency}' | '4X': currency = '{total_amount_sum.currency}']")

    if not total_amount.currency:
        raise Exception(f"Currency codes missing – ['00': currency = '{total_amount.currency}' | '4X': currency = '{total_amount_sum.currency}']")

    if total_amount != total_amount_sum:
        diff = abs(total_amount - total_amount_sum)
        raise Exception(f"Sums of amounts differ with {diff} – ['00': amount = {total_amount} | '4X': amount = {total_amount_sum}]")

    return amounts


amounts = get_transaction_amounts(example_content)
