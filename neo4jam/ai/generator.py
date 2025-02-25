import pandas as pd


def process_file(source: str, dest: str) -> None:
    df = pd.read_csv(source)
    df["cypher"] = df["text"].apply(lambda x: gen_cyphers(x))
    df.to_csv(dest, index=False)