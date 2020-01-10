import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num


def _read_csv(input_dir: str, filename: str) -> pd.DataFrame:
    return pd.read_csv(
        os.path.join(input_dir, filename),
        index_col="timestamp",
        parse_dates=True,
        squeeze=True,
    )


# def evaluate(input_dir: str, output_dir: str) -> None:
#     pd.plotting.register_matplotlib_converters()
#     datasets = ["trai", "vali", "test"]
#     models = ["linear", "lstm"]
#     y = {}
#     pred = {}
#     loss = {}
#     for d in datasets:
#         y[d] = _read_csv(input_dir, f"{d}_y.csv")
#     for m in models:
#         pred[m] = pd.concat(
#             [_read_csv(output_dir, f"pred_{d}_{m}.csv") for d in datasets]
#         )
#         loss[m] = pd.concat(
#             [_read_csv(output_dir, f"loss_{d}_{m}.csv") for d in datasets]
#         )
#     fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))
#     axs[0, 0].plot(pd.concat([y[d] for d in datasets]))
#     axs[0, 1].plot(pd.concat([y[d] for d in datasets]))
#     axs[0, 0].plot(
#         pred["linear"], linestyle="", marker=".", markersize=0.1,
#     )
#     axs[0, 1].plot(
#         pred["lstm"], linestyle="", marker=".", markersize=0.1,
#     )
#     axs[1, 0].fill_between(loss["linear"].index, loss["linear"])
#     axs[1, 1].fill_between(loss["lstm"].index, loss["lstm"])
#     axs[0, 0].axvline(y["vali"].index[0], linestyle=":", c="black")
#     axs[0, 0].axvline(y["test"].index[0], linestyle=":", c="black")
#     axs[1, 0].axvline(y["vali"].index[0], linestyle=":", c="black")
#     axs[1, 0].axvline(y["test"].index[0], linestyle=":", c="black")
#     axs[0, 1].axvline(y["vali"].index[0], linestyle=":", c="black")
#     axs[0, 1].axvline(y["test"].index[0], linestyle=":", c="black")
#     axs[1, 1].axvline(y["vali"].index[0], linestyle=":", c="black")
#     axs[1, 1].axvline(y["test"].index[0], linestyle=":", c="black")
#     # axs[1, 0].set_ylim(0, 0.35)
#     axs[1, 1].set_ylim(axs[1, 0].get_ylim())
#     axs[0, 1].legend(["truth", "prediction"])
#     axs[1, 0].text(
#         date2num(y["trai"].index[y["trai"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "training",
#         horizontalalignment="center",
#     )
#     axs[1, 0].text(
#         date2num(y["vali"].index[y["vali"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "validation",
#         horizontalalignment="center",
#     )
#     axs[1, 0].text(
#         date2num(y["test"].index[y["test"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "testing",
#         horizontalalignment="center",
#     )
#     axs[1, 1].text(
#         date2num(y["trai"].index[y["trai"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "training",
#         horizontalalignment="center",
#     )
#     axs[1, 1].text(
#         date2num(y["vali"].index[y["vali"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "validation",
#         horizontalalignment="center",
#     )
#     axs[1, 1].text(
#         date2num(y["test"].index[y["test"].shape[0] // 2]),
#         0.9 * axs[1, 0].get_ylim()[1],
#         "testing",
#         horizontalalignment="center",
#     )
#     axs[0, 0].set_xticks([])
#     axs[0, 1].set_xticks([])
#     axs[1, 0].set_xlabel("time")
#     axs[1, 1].set_xlabel("time")
#     axs[0, 0].set_ylabel("normalised price")
#     axs[1, 0].set_ylabel("loss")
#     axs[0, 0].set_title("Linear Model")
#     axs[0, 1].set_title("LSTM Model")
#     fig.subplots_adjust(hspace=0)


def _plot_scatters(
    output_dir: str, datasets: list, models: list, y: dict, pred: dict
) -> None:
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(16, 9))
    for di, d in zip(range(3), datasets):
        for mi, m in zip(range(2), models):
            axs[mi, di].scatter(y[d], pred[d, m])
    for ax in fig.get_axes():
        ax.label_outer()
    axs[1, 0].set_xlabel("train")
    axs[1, 1].set_xlabel("train")
    axs[1, 2].set_xlabel("train")
    axs[0, 0].set_ylabel("linear")
    axs[1, 0].set_ylabel("LSTM")
    plt.savefig(os.path.join(output_dir, "evaluate_scatters.png"))


def _plot_scatter(
    output_dir: str, datasets: list, models: list, y: dict, pred: dict
) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    for m in models:
        ax.scatter(y["test"], pred["test", m])
    ax.legend(models)
    ax.set_xlabel("truth")
    ax.set_ylabel("prediction")
    plt.savefig(os.path.join(output_dir, "evaluate_scatter.png"))


def _plot_loss(
    output_dir: str, datasets: list, models: list, y: dict, loss: dict
) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(pd.concat([loss[d, "linear"] for d in datasets]))
    ax.plot(pd.concat([loss[d, "lstm"] for d in datasets]))
    ax.axvline(y["vali"].index[0], linestyle=":", c="black")
    ax.axvline(y["test"].index[0], linestyle=":", c="black")
    ax.text(
        date2num(y["trai"].index[y["trai"].shape[0] // 2]),
        0.9 * ax.get_ylim()[1],
        "training",
        horizontalalignment="center",
    )
    ax.text(
        date2num(y["vali"].index[y["vali"].shape[0] // 2]),
        0.9 * ax.get_ylim()[1],
        "validation",
        horizontalalignment="center",
    )
    ax.text(
        date2num(y["test"].index[y["test"].shape[0] // 2]),
        0.9 * ax.get_ylim()[1],
        "testing",
        horizontalalignment="center",
    )
    ax.legend(models)
    ax.set_xlabel("time")
    ax.set_ylabel("MSE")
    fig.savefig(os.path.join(output_dir, "evaluate_loss.png"))


def evaluate(input_dir: str, output_dir: str) -> None:
    pd.plotting.register_matplotlib_converters()
    datasets = ["trai", "vali", "test"]
    models = ["linear", "lstm"]
    y = {}
    pred = {}
    loss = {}
    for d in datasets:
        y[d] = _read_csv(input_dir, f"{d}_y.csv")
    for m in models:
        for d in datasets:
            pred[d, m] = _read_csv(output_dir, f"pred_{d}_{m}.csv")
            loss[d, m] = _read_csv(output_dir, f"loss_{d}_{m}.csv")
    _plot_scatter(output_dir, datasets, models, y, pred)
    _plot_loss(output_dir, datasets, models, y, loss)
