"""Cleans up CSV files. Pass the file as a command-line argument.

For chat.csv, this will remove rows from offline chat, with a 5 minute buffer before and after stream was live.
"""
import math
import pandas as pd
import pathlib
import sys

args = sys.argv[1:]
path = pathlib.Path(args[0])

if path.name == "chat.csv":
    chat_df = pd.read_csv(path)
    stream_df = pd.read_csv(path.parent / "stream.csv")
    started_at = stream_df.iloc[0]["started_at"]
    last_row = stream_df.iloc[-1]
    ended_at = last_row["duration"] + started_at
    size_before = path.stat().st_size
    chat_df = chat_df[
        chat_df["minute"].between(
            math.floor(started_at / 60) - 5, math.ceil(ended_at / 60) + 5
        )
    ]
    chat_df.to_csv(path, index=False)
    size_after = path.stat().st_size
    if size_before != size_after:
        print(
            f"Cleaned up: {path}. Reduced size from {size_before} bytes to {size_after} bytes."
        )
    else:
        print(f"Nothing to clean up: {path}.")
else:
    raise NotImplementedError(f"clean_csv can't clean {path.name}.")
