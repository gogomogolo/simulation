import matplotlib.pyplot as plt


def create_plot(title, xlabel, ylabel):
    plt.plot()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt


def clear_plot(plot):
    plot.gcf().clear()
    plot.clf()


def add_line_to_plot(plot, line):
    x_axis_identifier = getattr(line, 'x_id')
    y_axis_identifier = getattr(line, 'y_id')
    data_frame = getattr(line, 'data_frame')
    color = getattr(line, 'color')
    width = getattr(line, 'width')
    plot.plot(x_axis_identifier, y_axis_identifier, data=data_frame, color=color, linewidth=width)


def show_plot(plot):
    plot.legend()
    plot.tight_layout()
    plot.show()


def write_plot_to_file(plot, path):
    plot.legend()
    plot.tight_layout()
    plot.savefig(path)



