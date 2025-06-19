import urllib.request
import urllib.error
import json
from config import MIDI_DEVICE_NAME, TOKENS
import mido
import threading
import sys

channel_id = int(sys.argv[-1])


def player(sound_id: str, source_guild_id: str, token: str):
    url = f"https://discord.com/api/v10/channels/{channel_id}/send-soundboard-sound"

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "Python/3.10 (urllib)",
    }

    data = {
        "sound_id": sound_id,
    }
    if source_guild_id:
        data["source_guild_id"] = source_guild_id

    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=1) as response:
            print("SUCCESS", response)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP Error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except TimeoutError:
        pass
    except Exception as e:
        print(f"Generic error {e!r}")


note_map = {}
for i in range(21, 109):
    octave = (i // 12) - 1
    base_note = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"][
        i % 12
    ]
    note_map[i] = f"{base_note}{octave}"

with open("sounddb.json") as fd:
    sounds = json.load(fd)

idx = 0

threads = []

try:
    with mido.open_input(name=MIDI_DEVICE_NAME) as inport:
        for msg in inport:
            if msg.type == "note_on":
                print("Playing Note", note_map[msg.note], msg)
                s = sounds[note_map[msg.note]]
                th = threading.Thread(target=player, args=(s[0], s[1], TOKENS[idx]))
                threads.append(th)
                th.start()
                idx += 1
                idx = idx % len(TOKENS)
except (Exception, KeyboardInterrupt):
    for thread in threads:
        thread.join(timeout=0.5)
    raise
