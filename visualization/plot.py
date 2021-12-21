# Import
import warnings
from pathlib import Path
from typing import List, Union
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Static variable
COLOUR_LIST: List[str] = ["deepskyblue", "blue", "lightgreen", "g", "gold", "orange", "magenta", "white"]


def boxplot(data: List[List[List[float]]], labels: List[List[str]], title: str,
            x_label: Union[str, None] = None, y_label: Union[str, None] = None, legend: Union[List[str], None] = None,
            save_path: [str, Path, None] = None, show: bool = True, showfliers: bool = True, showmeans: bool = True) -> None:
    fig, ax = plt.subplots()

    try:
        # Boxplot
        position_temp = 1
        for i, group in enumerate(data):
            end_position_end = position_temp + 1
            ax.boxplot(x=group,
                       showfliers=showfliers,
                       positions=list(range(position_temp, end_position_end)),
                       labels=labels[i],
                       widths=0.5,
                       medianprops={"color": "red"},
                       showmeans=showmeans,
                       meanprops={"marker": ".",
                                  "markerfacecolor": "red",
                                  "markeredgecolor": "black",
                                  "markersize": "8"},
                       patch_artist=True,
                       boxprops={"facecolor": COLOUR_LIST[i],
                                 "color": "black"}
                       )
            position_temp = end_position_end

        # Legend
        if legend is not None:
            custom_lines = []
            for color in COLOUR_LIST:
                custom_lines.append(Line2D([0], [0], color=color, lw=4))

            ax.legend(custom_lines[0:len(legend)], legend, loc="upper right")

        # Title and labels
        ax.set_title(title)
        if x_label is not None:
            ax.set_xlabel(x_label)
        if y_label is not None:
            ax.set_ylabel(y_label)

        plt.tight_layout()

        if save_path is not None:
            plt.savefig(save_path, dpi=500)

        if show:
            plt.show()
    except ValueError:
        warnings.warn("boxplot - invalid data!", category=Warning)
    except Exception:
        warnings.warn("boxplot - something wrong!", category=Warning)
    finally:
        plt.close(fig)


def scatter(data_x: Union[List[float], List[List[float]]], data_y: Union[List[float], List[List[float]]], title: str,
            x_label: Union[str, None] = None, y_label: Union[str, None] = None, labels: Union[List[List[str]], None] = None,
            point_label: Union[List[str], List[List[str]], None] = None, save_path: [str, Path, None] = None,
            show: bool = True, log_scale: bool = False) -> None:
    fig, ax = plt.subplots()

    try:
        point_label_temp = None

        # List[List[float]]
        if len(data_x) and isinstance(data_x[0], list):
            data_x_temp, data_y_temp = data_x, data_y

            if point_label is not None:
                point_label_temp = point_label
        # List[float]
        else:
            data_x_temp, data_y_temp = [data_x], [data_y]

            if point_label is not None:
                point_label_temp = [point_label]

        for i in range(len(data_x_temp)):
            ax.scatter(x=data_x_temp[i], y=data_y_temp[i],
                       s=50,
                       label="" if labels is None else labels[i],
                       color=COLOUR_LIST[i],
                       edgecolors="black")

        if point_label_temp is not None:
            for i in range(len(data_x_temp)):
                for j, annotation in enumerate(point_label_temp[i]):
                    ax.annotate(annotation, (data_x_temp[i][j], data_y_temp[i][j]))

        # Diagonal line
        ax.axline((1, 1), slope=1, color="red", ls='--')

        # Title and labels
        ax.set_title(title)
        if x_label is not None:
            ax.set_xlabel(x_label)
        if y_label is not None:
            ax.set_ylabel(y_label)

        if labels is not None:
            ax.legend()

        if log_scale:
            ax.set_xscale('log')
            ax.set_yscale('log')

        plt.tight_layout()

        if save_path is not None:
            plt.savefig(save_path, dpi=500)

        if show:
            plt.show()
    except Exception:
        warnings.warn("scatter - something wrong!", category=Warning)
    finally:
        plt.close(fig)


def histogram(data: Union[List[float], List[List[float]]], labels: List[str], title: str,
              x_label: Union[str, None] = None, y_label: Union[str, None] = None, bins: int = 10,
              save_path: [str, Path, None] = None, show: bool = True) -> None:
    fig, ax = plt.subplots()

    try:
        ax.hist(data, bins=bins)
        plt.legend(labels)

        # Title and labels
        ax.set_title(title)
        if x_label is not None:
            ax.set_xlabel(x_label)
        if y_label is not None:
            ax.set_ylabel(y_label)

        plt.tight_layout()

        if save_path is not None:
            plt.savefig(save_path, dpi=500)

        if show:
            plt.show()
    except Exception:
        warnings.warn("histogram - something wrong!", category=Warning)
    finally:
        plt.close(fig)
