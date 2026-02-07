This dataset contains a curated catalog of skills for various LLMs and AI agents, extracted from the `antigravity-awesome-skills` repository.

## Dataset Structure

The dataset consists of the following files:

- **`skills.csv`**: The main data file containing the skills list.
- **`datapackage.yaml`**: Frictionless Data metadata describing the dataset schema.
- **`generate_dataset.py`**: A Python script used to generate individual CSV files from the source `skills_index.json` and `CATALOG.md`.

## Generation

To regenerate this dataset from the source files:

1.  Ensure you have `skills_index.json` and `CATALOG.md` in the parent directory.
2.  Run the generation script:

    ```bash
    python3 generate_dataset.py
    ```

## License

CC0 1.0 Universal - Public Domain Dedication
