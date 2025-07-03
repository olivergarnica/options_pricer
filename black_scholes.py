import math

class BlackScholes:

    @staticmethod
    def call_price(S, K, T, r, sigma):
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        N_d1 = BlackScholes._norm_cdf(d1)
        N_d2 = BlackScholes._norm_cdf(d2)
        perShare = (S * N_d1 - K * math.exp(-r * T) * N_d2)
        return perShare
    
    @staticmethod
    def put_price(S, K, T, r, sigma):
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        N_d1 = BlackScholes._norm_cdf(-d1)
        N_d2 = BlackScholes._norm_cdf(-d2)
        perShare =  (K * math.exp(-r * T) * N_d2 - S * N_d1)
        return perShare
    
    @staticmethod
    def _norm_cdf(x):
        """Calculate the cumulative distribution function for a standard normal distribution."""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    
