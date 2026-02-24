def generate_schedule(mortgage,
                      extra_payment=0,
                      lump_sum=0,
                      lump_sum_month=0):
    
    balance = mortgage.principal
    payment = mortgage.emi()
    r = mortgage.periodic_rate()
    schedule = []

    for period in range(1, mortgage.total_payments() + 1):
        interest = balance * r
        principal = payment - interest

        principal += extra_payment

        if lump_sum and period == lump_sum_month:
            principal += lump_sum
        
        if principal > balance:
            principal = balance
        
        balance -= principal

        schedule.append({
            "period":period,
            "payment":payment + extra_payment,
            "principal":principal,
            "interest":interest,
            "balance":balance
        })

        if balance <= 0:
            break
    
    return schedule