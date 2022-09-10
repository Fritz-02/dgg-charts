import json
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import webbrowser

with open("config.json") as f:
    config = json.load(f)


date = "22-09-09"
df = pd.read_csv(f"data/{date}/stream.csv")
df.drop_duplicates(subset='duration', keep="first", inplace=True)
df["minute"] = ((df["started_at"] + df["duration"]) / 60).astype("int32")
chat_df = pd.read_csv(f"data/{date}/chat.csv")[1:-1]

df = pd.merge(df, chat_df, on='minute', how='outer')
df["sma5_msg_count"] = df["msg_count"].rolling(5).mean()

df["viewer_diff"] = df["viewers"].diff()
duration_diff = df["duration"].diff()
df["viewer_vel"] = (df["viewer_diff"] / duration_diff).round(3)
df["viewer_acc"] = (df["viewer_vel"].diff() / duration_diff).round(3)
df["viewer_vel"] = df["viewer_vel"] * 60
df["viewer_acc"] = df["viewer_acc"] * 60
df["viewer_change"] = df["viewers"].pct_change() * 100

df["duration_s"] = df["duration"]
df["duration"] = df["duration"].apply(pd.to_datetime, unit="s")

# plotting
plt.style.use('seaborn-dark')
fig, axs = plt.subplots(2 if config["chart"]["message_count"] else 1, gridspec_kw={'height_ratios': [5, 1]})

fig.subplots_adjust(right=0.75)

p1, = axs[0].plot(df["duration"], df["viewers"], "b-", label="Viewers")
handles = [p1]

axs[0].set_xlim(0, df["duration"].max())
axs[0].set_ylim(df["viewers"].min(), df["viewers"].max())
axs[0].set_xlabel("Duration (s)")
axs[0].set_ylabel("Viewers")

axs[0].yaxis.label.set_color(p1.get_color())

tkw = dict(size=4, width=1.5)
axs[0].tick_params(axis='y', colors=p1.get_color(), **tkw)
axs[0].tick_params(axis='x', **tkw)
# axs[0].set_xticks(np.arange(0, df["duration"].max() + 1, 1800.0))
axs[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
minlocator = dates.MinuteLocator(byminute=[0, 15, 30, 45])
# minlocator = dates.MinuteLocator(byminute=[0, 10, 20, 30, 40, 50])
# axs[0].xaxis.set_major_locator(minlocator)


def on_dblclick(event):
    """Double-clicking on the chart will open the VOD at the clicked specific time."""
    if event.dblclick and event.xdata is not None:
        ts = int(event.xdata * 86400)
        video_id = df.iloc[(df['duration_s'] - ts).abs().argsort()[0]]["video_id"]
        webbrowser.open(f"https://youtu.be/{video_id}?t={ts}")


cid = fig.canvas.mpl_connect("button_press_event", on_dblclick)


def make_plot(y, marker, label: str, ylim: tuple, spine_position: float = 1, axhline: int = None, *, axis_label: bool = True,
              ax: int = 0, add_handle: bool = True):
    twinx = axs[ax].twinx()
    twinx.spines.right.set_position(("axes", spine_position))
    p, = twinx.plot(df["duration"], y, marker, label=label)
    twinx.set_ylim(*ylim)
    twinx.set_ylabel(label)
    if axis_label:
        twinx.yaxis.label.set_color(p.get_color())
    else:
        twinx.axis('off')
    twinx.tick_params(axis='y', colors=p.get_color(), **tkw)
    if add_handle:
        handles.append(p)
    if axhline is not None:
        twinx.axhline(axhline)
    return p





if config["chart"]["pct_change"]:
    make_plot(df["viewer_change"], "k-", "Viewer difference (%)", (-10, 10), 1.0)
    axs[0].fill_between(
        x=df["duration"],
        y1=df["viewers"],
        y2=0,
        where=(df["viewer_change"] <= -2),
        facecolor="lightcoral",
        alpha=0.5
    )


if config["chart"]["viewer_velocity"]:
    df["sma15_viewer_vel"] = df["viewer_vel"].rolling(15).mean()
    df["ema15_viewer_vel"] = df["viewer_vel"].ewm(span=15, adjust=False).mean()

    vel_lim = max(abs(df["viewer_vel"].min()), df["viewer_vel"].max()) * 1.05
    # make_plot(df["viewer_vel"], "g-", "Viewers/minute", (-vel_lim, vel_lim), 1.0, axhline=0)

    # make_plot(df["sma15_viewer_vel"], "r--", "Viewers/minute (SMA15)", (-vel_lim, vel_lim), axis_label=False)
    # make_plot(df["ema15_viewer_vel"], "r-", "Viewers/minute (EMA15)", (-vel_lim, vel_lim), axis_label=False)
    make_plot(df["ema15_viewer_vel"], "r-", "Viewers/minute (EMA15)", (-vel_lim, vel_lim), 1.0, axhline=0)


    # ax.fill_between(range(len(df)), min(df), max(df), where=(df["viewer_vel"] < 0), alpha=0.5)
    # axs[0].fill_between(
    #     x=df["duration"],
    #     y1=df["viewers"],
    #     y2=0,
    #     where=(df["ema15_viewer_vel"] < -50),
    #     facecolor="lightcoral",
    #     alpha=0.5
    # )


if config["chart"]["viewer_acceleration"]:
    acc_lim = max(abs(df["viewer_acc"].min()), df["viewer_acc"].max()) * 1.05
    make_plot(df["viewer_acc"], "m-", "Viewers/minute^2", (-acc_lim, acc_lim), 1.1)

    # twin2 = ax.twinx()
    # twin2.spines.right.set_position(("axes", 1.1))
    # p3, = twin2.plot(df["duration"], df["viewer_acc"], "m-", label="Viewers/minute^2")
    # twin2.set_ylim(-acc_lim, acc_lim)
    # twin2.set_ylabel("Viewers/minute^2")
    # twin2.yaxis.label.set_color(p3.get_color())
    # twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    # twin2.axhline(0)

    # ax.fill_between(
    #     x=df["duration"],
    #     y1=df["viewers"],
    #     y2=0,
    #     where=(df["viewer_acc"] < -2),
    #     facecolor="lightcoral",
    #     alpha=0.5
    # )
    # handles.append(p3)

if config["chart"]["message_count"]:
    p20, = axs[1].plot(df["duration"], df["msg_count"], "y-", label="Messages/minute")

    axs[1].set_xlim(0, df["duration"].max())
    axs[1].set_ylim(0, df["msg_count"].max())
    axs[1].set_xlabel("Duration (s)")
    axs[1].set_ylabel("Messages/minute")

    axs[1].yaxis.label.set_color(p20.get_color())

    # tkw = dict(size=4, width=1.5)
    axs[1].tick_params(axis='y', colors=p20.get_color(), **tkw)
    axs[1].tick_params(axis='x', **tkw)
    axs[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    axs[1].xaxis.set_major_locator(minlocator)

    # axs[1].set_xticks(np.arange(0, df["duration"].max() + 1, 1800.0))

    p21 = make_plot(df["sma5_msg_count"], "k--", "Messages/minute (SMA5)", (0, df["msg_count"].max()), axis_label=False,
                    ax=1, add_handle=False)

    axs[1].legend(handles=[p20, p21])


def convert_time(s: str) -> int:
    hour, minute, second = s.split(":")
    return (int(hour) * 60 + int(minute)) * 60 + int(second)


def add_text(r: pd.Series):
    print(type(r))
    center = pd.Timedelta(r.end_ts - r.start_ts)
    axs[0].text(
        r.start_ts + center / 2, df["viewers"].min() + 50,
        r.topic,
        rotation=90
    )


def add_axvspan(r, color: str, alpha: float = 0.5):
    axs[0].axvspan(r.start_ts, r.end_ts, alpha=alpha, color=color)
    axs[1].axvspan(r.start_ts, r.end_ts, alpha=alpha, color=color)


if config["chart"]["lwod"]:
    # read times from csv
    lwod_df = pd.read_csv(f"data/{date}/lwod.csv")
    lwod_df["start_ts"] = lwod_df["start"].apply(convert_time).apply(pd.to_datetime, unit="s")
    lwod_df["end_ts"] = lwod_df["end"].apply(convert_time).apply(pd.to_datetime, unit="s")
    for _, row in lwod_df.iterrows():
        if "AFK" in row.topic:
            add_axvspan(row, "lightcoral")
        elif row.topic.startswith("Talking with"):
            add_axvspan(row, "aqua")
            add_text(row)
        elif row.topic.startswith("Debating"):
            add_axvspan(row, "blue")
            add_text(row)
        elif row.topic.startswith("Viewer Call-ins"):
            add_axvspan(row, "green")
            add_text(row)
        elif any(row.topic.startswith(x) for x in ("Talking", "Reading", "Watching")):
            add_axvspan(row, "khaki")
            add_text(row)


axs[0].legend(handles=handles)
plt.show()
