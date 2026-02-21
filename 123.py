import json

# 假設你的 JSON 存在 data.json
with open("lastest.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for key, value in data.items():
    if value.get("album") is None:
        track_name = value.get("track")
        artist_name = value.get("artist")
        # 跳提示
        ans = input(f"{artist_name} - {track_name} 的 album 是空的，要用 track 名稱補上嗎？(y/n): ").strip().lower()
        if ans == "y":
            value["album"] = track_name

# 存回 JSON
with open("data_updated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False,separators=(',', ':'), indent=2)

print("完成更新！")