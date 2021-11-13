import numpy as np
import matplotlib.pyplot as plt


def generate_single_scatter_plots(coordinates, data_set_names, bool_mask, fingerprint_names, path):
    area = np.pi * 2

    plt.scatter(x=coordinates[np.invert(bool_mask), 0], y=coordinates[np.invert(bool_mask), 1], c="green", s=area)
    plt.scatter(x=coordinates[bool_mask, 0], y=coordinates[bool_mask, 1], c="red", s=area)
    plt.title(f"{data_set_names} - {fingerprint_names}")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(f"{path}{data_set_names} - {fingerprint_names}_ChemChar_Plot.png")
    plt.show()


def generate_scatter_plots_to_concatenate(fig, gs, coordinates, data_set_names, fingerprint_names, row, column,
                                          bool_mask, path):
    area = np.pi * 1
    plt.gcf().set_size_inches((15, 15))

    ax = fig.add_subplot(gs[row, column])

    ax.scatter(x=coordinates[np.invert(bool_mask), 0], y=coordinates[np.invert(bool_mask), 1], c='green', s=area)
    ax.scatter(x=coordinates[bool_mask, 0], y=coordinates[bool_mask, 1], c='red', s=area)

    ax.set_title(f"{data_set_names} - {fingerprint_names}")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.savefig(f"{path}ChemChar_Plot.png")


def generate_chemcharts_scatter_plot(data_sets, path, scatter_plot_type="single_scatterplots"):
    fig = plt.figure()
    n_rows = len(data_sets[0].fingerprint_lists)
    n_columns = len(data_sets)
    gs = fig.add_gridspec(n_rows, n_columns)

    for ind_sets in range(n_columns):
        data_set_names = data_sets[ind_sets].name

        for ind_embedding in range(n_rows):
            embedding = data_sets[ind_sets].embedding_lists[ind_embedding]
            fingerprint_names = data_sets[ind_sets].fingerprint_lists[ind_embedding].name
            bool_mask = np.array(data_sets[ind_sets].active_inactive_list)

            if scatter_plot_type == "single_scatterplots":
                generate_single_scatter_plots(embedding.np_array, data_set_names, bool_mask, fingerprint_names, path)
            elif scatter_plot_type == "concatenated_scatterplots":
                generate_scatter_plots_to_concatenate(fig, gs, embedding.np_array, data_set_names, fingerprint_names,
                                                      ind_embedding, ind_sets, bool_mask, path)
                fig.show()
            else:
                print("fail!!!!!")
