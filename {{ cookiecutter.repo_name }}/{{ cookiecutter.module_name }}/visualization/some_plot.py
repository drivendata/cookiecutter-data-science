from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "some_dataset.csv",
    output_path: Path = FIGURES_DIR / "some_plot.png",
):
    logger.info("Generating some plot from some data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")


if __name__ == "__main__":
    app()
