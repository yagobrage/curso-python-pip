import matplotlib.pyplot as plt

def generate_pie_chart():
    labels = ['a','b','c']
    values = [10,5,18]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels)
    plt.savefig('pie.png')
    plt.close()