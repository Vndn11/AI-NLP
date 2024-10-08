import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('IMDB Dataset.csv')

total_reviews = len(df)
split_index = int(total_reviews * (70/100))

train_df = df[:split_index]
test_df = df[split_index:]



def plot_label_distribution(df, title, plot_type="pie"):
    label_counts = df['sentiment'].value_counts()
    labels = label_counts.index
    sizes = label_counts.values
    percentages = 100*label_counts/len(df)
    
    if plot_type == "pie":
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    else:  # Bar chart
        fig, ax = plt.subplots()
        ax.bar(labels, sizes, tick_label=labels)
        ax.set_ylabel('Number of Samples')
        ax.set_title(title)
        
        # Adding the text labels on the bars
        for i in range(len(labels)):
            ax.text(i, sizes[i] + 0.05*max(sizes), f'{percentages[i]:.1f}%\n({sizes[i]})', ha='center')
    
    plt.title(title)
    plt.show()


plot_label_distribution(df, "Complete Dataset Label Distribution", plot_type="pie")

plot_label_distribution(train_df, "Training Set Label Distribution", plot_type="pie")

plot_label_distribution(test_df, "Test Set Label Distribution", plot_type="pie")

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Training set
train_label_counts = train_df['sentiment'].value_counts()
train_labels = train_label_counts.index
train_sizes = train_label_counts.values
train_percentages = 100*train_label_counts/len(train_df)

axs[0].bar(train_labels, train_sizes, color='skyblue')
axs[0].set_title('Training Set Label Distribution')
for i, label in enumerate(train_labels):
    axs[0].text(i, train_sizes[i] + 0.05*max(train_sizes), f'{train_percentages[label]:.1f}%\n({train_sizes[i]})', ha='center')

# Test set
test_label_counts = test_df['sentiment'].value_counts()
test_labels = test_label_counts.index
test_sizes = test_label_counts.values
test_percentages = 100*test_label_counts/len(test_df)

axs[1].bar(test_labels, test_sizes, color='lightgreen')
axs[1].set_title('Test Set Label Distribution')
for i, label in enumerate(test_labels):
    axs[1].text(i, test_sizes[i] + 0.05*max(test_sizes), f'{test_percentages[label]:.1f}%\n({test_sizes[i]})', ha='center')

plt.tight_layout()
plt.show()
