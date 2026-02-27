def generate_schedule(
    mortgage,
    extra_payment: float = 0.0,
    lump_sum: float = 0.0,
    lump_sum_month: int = 0,
) -> list[dict]:
    """
    Generate a full amortization schedule.

    Parameters
    ----------
    mortgage        : Mortgage dataclass instance
    extra_payment   : additional amount added to every monthly payment
    lump_sum        : one-time prepayment applied at lump_sum_month
    lump_sum_month  : period number at which the lump sum is applied
    """
    balance  = mortgage.principal
    base_emi = mortgage.emi()
    r        = mortgage.periodic_rate()
    schedule = []

    for period in range(1, mortgage.total_payments() + 1):
        interest  = balance * r
        principal = base_emi - interest + extra_payment

        # Apply one-time lump sum at the chosen month
        if lump_sum and period == lump_sum_month:
            principal += lump_sum

        # Cap principal so we never overpay on the final instalment
        if principal >= balance:
            principal    = balance
            actual_payment = principal + interest
            balance      = 0.0
        else:
            actual_payment = base_emi + extra_payment
            balance       -= principal

        schedule.append({
            "period":    period,
            "payment":   round(actual_payment, 2),
            "principal": round(principal,      2),
            "interest":  round(interest,       2),
            "balance":   round(balance,        2),
        })

        if balance <= 0:
            break

    return schedule