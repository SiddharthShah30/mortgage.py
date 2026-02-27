from dataclasses import dataclass


@dataclass
class Mortgage:
    principal: float
    annual_rate: float
    years: int
    payments_per_year: int = 12

    def periodic_rate(self) -> float:
        return self.annual_rate / 100 / self.payments_per_year

    def total_payments(self) -> int:
        return self.years * self.payments_per_year

    def emi(self) -> float:
        r = self.periodic_rate()
        n = self.total_payments()
        p = self.principal

        if r == 0:
            return p / n

        return p * r * (1 + r) ** n / ((1 + r) ** n - 1)