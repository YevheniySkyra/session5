import pandas as pd
import numpy as np

participants = pd.read_csv('participants.csv')  # Let's load in our participant data!

# We can use a for loop to go through this participant list and load in all the trials into a single dataframe.
trials = pd.DataFrame()
for participant_id in participants['id']:
    trials = trials.append(pd.read_csv(f'participants/{participant_id}.csv'))

# Alternatively, you could loop over the files in the participants directory.
# from pathlib import Path  # noqa: E402
# trials = pd.DataFrame()
# for file in Path('participants').iterdir():
#     trials = trials.append(pd.read_csv(f'participants/{file.name}'))

# Now, let's merge the participant and trial data, so we have them all in a single dataframe!
trials = trials.merge(participants, on='id')
trials.rename(columns={'Unnamed: 0': 'trial_order'}, inplace=True)  # Rename the unnamed column, representing the trial order
trials.to_csv('merged.csv')  # Save the output to a file

# The function below was to answer someone's question about using your own function with dataframes; see below!
# def mean_minus_2(data):
#     return np.mean(data) - 2

# There are different ways in which you can group and aggregate data:
# summary = trials.groupby(by='condition').aggregate([np.mean, np.std])  # This applies the specified functions to all columns
# summary = trials.groupby(by='condition').describe()  # This applies some default aggregation functions to all columns

# The method below allows you to specify exactly which columns to aggregate, using what function, and what the new column name should be:
summary = trials.groupby(by='condition').aggregate(  # for multiple columns, use ['id', 'condition'] instead of just 'id'
    mean_RT=pd.NamedAgg('RT', np.mean),
    std_RT=pd.NamedAgg('RT', np.std),
    mean_age=pd.NamedAgg('age', np.mean)  # lambda data: np.mean(data) - 2
)

# Use the method below if you have an old version of Pandas, and don't have access to NamedAgg
# summary = trials.groupby(by='condition').aggregate({
#     'RT': [np.mean, np.std]
# })
# summary.columns = ['_'.join(column) for column in summary.columns.values]

# After grouping, condition will be part of the index, which makes that pandas treats it differently from other columns.
# To prevent this, you can reset the index:
summary.reset_index(inplace=True)
print(summary)

# Let's use matplotlib to make a simple plot!
from matplotlib import pyplot as plt  # noqa: E402

plt.figure()
plt.bar(summary['condition'], summary['mean_RT'])
plt.errorbar(summary['condition'], summary['mean_RT'], summary['std_RT'], fmt='.k')
plt.show()

# Let's use Seaborn to use a slightly more complex plot!
import seaborn as sns  # noqa: E402
sns.boxplot(x='id', y='RT', hue='condition', data=trials)
plt.show()  # We still need matplotlib to actually open the window and view the plot

# Finally, let's use ggplot in Python using plotnine!
import plotnine as gg  # noqa: E402
from plotnine import ggplot  # noqa: E402
plot = (ggplot(gg.aes(x='condition', y='RT'), data=trials) +  # In ggplot, you specify visualization-data bindings using gg.aes
        gg.geom_boxplot(gg.aes(fill='condition')) +  # You can use the + operator to add different geoms to your plot
        gg.facet_wrap('id')  # And other methods like facet_wrap, to e.g. create a faceted plot (here for different participants)
        )
# plot.save('plot.pdf')  # You can use this to save the plot to a file
plot.draw()
plt.show()  # We still need matplotlib to actually open the window and view the plot
