def generate_schedule(mortgage):
    balance = mortgage.principal
    payment = mortgage.emi()
    r = mortgage.periodic_rate()
    schedule = []

    for period in range(1, mortgage.total_payments() + 1):
        interest = balance * r
        principal = payment - interest
        balance -= principal

        if balance < 0:
            principal += balance
            balance = 0

        schedule.append({
            "period": period,
            "payment": payment,
            "principal": principal,
            "interest": interest,
            "balance": balance
        })

        if balance == 0:
            break

    return schedule