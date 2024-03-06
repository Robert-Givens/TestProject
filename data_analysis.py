import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

finaldata = pd.read_csv("final_data.csv")

# Summary statistics - Python doesn't have a direct equivalent to `stargazer` for pretty tables in console output,
# but you can use `describe()` for basic summaries or the `summary_col` function from `statsmodels` for regression summaries.

# Relationship between wins & injuries
tab = finaldata.groupby('win')['out'].mean().reset_index()
sns.barplot(x='win', y='out', data=tab)
plt.show()

# Correlation table
print(finaldata[['win', 'out', 'age', 'lag_win_perc']].corr())

# Regression analysis
formula = "win ~ out"
lm_model1 = smf.ols(formula, data=finaldata).fit()

# Repeat for other models, adjusting the formula as necessary

# Print summaries
print(lm_model1.summary())
# Repeat for other models
