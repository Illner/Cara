# Import
import warnings
from pathlib import Path
from typing import List, Union
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Static variable
COLOUR_LIST: List[str] = ["cornflowerblue", "green", "orange", "magenta", "gold", "lime"]


def boxplot(data: List[List[List[float]]], labels: List[List[str]], title: str,
            x_label: Union[str, None] = None, y_label: Union[str, None] = None, legend: Union[List[str], None] = None,
            save_path: [str, Path, None] = None, show: bool = True) -> None:
    try:
        _, ax = plt.subplots()

        # Boxplot
        position_temp = 1
        for i, group in enumerate(data):
            end_position_end = position_temp + len(group)
            ax.boxplot(x=group,
                       positions=list(range(position_temp, end_position_end)),
                       labels=labels[i],
                       widths=0.5,
                       medianprops={"color": "red"},
                       showmeans=True,
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
            plt.savefig(save_path, dpi=1000)

        if show:
            plt.show()
    except ValueError:
        warnings.warn("boxplot - invalid data!", category=Warning)
    except:
        warnings.warn("boxplot - something wrong!", category=Warning)


def scatter(data_x: List[float], data_y: List[float], title: str,
            x_label: Union[str, None] = None, y_label: Union[str, None] = None,
            save_path: [str, Path, None] = None, show: bool = True) -> None:
    _, ax = plt.subplots()
    ax.scatter(x=data_x, y=data_y,
               s=50,
               color=COLOUR_LIST[0],
               edgecolors="black")

    # Diagonal line
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, color="red", ls='--')

    # Title and labels
    ax.set_title(title)
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=1000)

    if show:
        plt.show()
