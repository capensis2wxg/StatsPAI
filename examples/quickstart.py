import numpy as np
import pandas as pd
import statspai as sp


rng = np.random.default_rng(42)
n = 500
education = rng.normal(12, 2, n)
experience = rng.uniform(0, 40, n)
wage = 2 + 0.8 * education + 0.05 * experience + rng.normal(0, 2, n)

df = pd.DataFrame(
    {
        "wage": wage,
        "education": education,
        "experience": experience,
    }
)

result = sp.regress("wage ~ education + experience", data=df, robust="hc1")
print(result.summary())
