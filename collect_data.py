from datetime import datetime
from dggbot import DGGChat, Message
import json
import pandas as pd
from pathlib import Path
from pprint import pprint
import time
import threading

today = datetime.today().strftime("%y-%m-%d")
viewer_df = pd.DataFrame(
    {
        "timestamp": pd.Series(dtype="int"),
        "video_id": pd.Series(dtype="str"),
        "viewers": pd.Series(dtype="int"),
        "started_at": pd.Series(dtype="int"),
        "duration": pd.Series(dtype="int"),
        "status_text": pd.Series(dtype="str"),
        "url": pd.Series(dtype="str"),
    }
)
chat_df = pd.DataFrame(columns=["minute", "msg_count"], dtype="int64")

# for df, fp in ((viewer_df, f"data/streamdata_{today}.csv"), (chat_df, f"data/chatdata_{today}.csv")):
#     if Path(fp).exists():
#         df = pd.concat([df, pd.read_csv(fp)], axis=0, ignore_index=True)

Path(f"data/{today}").mkdir(parents=True, exist_ok=True)

if Path(fp := f"data/{today}/stream.csv").exists():
    viewer_df = pd.concat([viewer_df, pd.read_csv(fp)], axis=0, ignore_index=True)

if Path(fp := f"data/{today}/chat.csv").exists():
    chat_df = pd.concat([chat_df, pd.read_csv(fp)], axis=0, ignore_index=True)


class DGGLive(DGGChat):
    WSS = "wss://live.destiny.gg"
    FILE = f"data/{today}/stream.csv"
    is_live = False

    def _on_message(self, ws, message: str):
        data = json.loads(message)
        if (type_ := data["type"]) == "dggApi:streamInfo":
            stream = data["data"]["streams"]["youtube"]
            self.is_live = stream["live"]
            if self.is_live:
                print(stream["duration"])
                started_at = int(
                    datetime.strptime(
                        stream["started_at"], "%Y-%m-%dT%H:%M:%S%z"
                    ).timestamp()
                )
                viewer_df.loc[len(viewer_df)] = [
                    int(datetime.now().timestamp()),
                    stream["id"],
                    stream["viewers"],
                    started_at,
                    stream["duration"],
                    stream["status_text"],
                    f"https://youtu.be/{stream['id']}?t={stream['duration']}",
                ]
                viewer_df.to_csv(self.FILE, index=False)
        elif type_ in ("dggApi:youtubeVideos", "dggApi:youtubeVods"):
            pass
        else:
            pprint(data, indent=2, sort_dicts=False)


live = DGGLive()
chat = DGGChat()


@chat.event()
def on_msg(msg: Message):
    # if not live.is_live:
    #     return
    minute = int(msg.timestamp / 60000)
    if minute in chat_df["minute"].unique():
        chat_df.loc[chat_df["minute"] == minute, "msg_count"] += 1
    else:
        chat_df.to_csv(f"data/{today}/chat.csv", index=False)
        chat_df.loc[len(chat_df)] = [minute, 1]


def thread(ws: DGGChat):
    while True:
        print(f"{ws.__class__.__name__} connected")
        ws.run()
        time.sleep(1)


c = threading.Thread(target=thread, args=(chat,), daemon=True)
l = threading.Thread(target=thread, args=(live,), daemon=True)
c.start()
l.start()
input("Press ENTER to close...")
