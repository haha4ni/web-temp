#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音樂檔案藝術家統計分析工具
分析單一JSON檔案，統計藝術家分佈和總條目數
"""

import json
import sys
from pathlib import Path

def load_json_file(file_path):
    """載入JSON檔案"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"錯誤：JSON檔案格式錯誤 {file_path} - {e}")
        return None
    except Exception as e:
        print(f"錯誤：讀取檔案失敗 {file_path} - {e}")
        return None

def analyze_artists(music_data, show_top=10):
    """分析藝術家統計"""
    print(f"\n=== 音樂檔案統計分析 ===")
    print(f"總條目數: {len(music_data)}")
    
    # 統計藝術家分佈
    artist_count = {}
    album_count = {}
    track_without_artist = 0
    track_without_album = 0
    
    for entry_id, entry_data in music_data.items():
        # 藝術家統計
        artist = entry_data.get('artist', '未知藝術家')
        if artist == '' or artist is None:
            artist = '未知藝術家'
            track_without_artist += 1
        artist_count[artist] = artist_count.get(artist, 0) + 1
        
        # 專輯統計
        album = entry_data.get('album', '未知專輯')
        if album == '' or album is None:
            album = '未知專輯'
            track_without_album += 1
        album_count[album] = album_count.get(album, 0) + 1
    
    # 顯示藝術家統計 (Top N)
    print(f"\n=== 藝術家統計 (Top {show_top}) ===")
    sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
    
    for i, (artist, count) in enumerate(sorted_artists[:show_top], 1):
        percentage = (count / len(music_data)) * 100
        print(f"{i:2d}. {artist}: {count} 首 ({percentage:.1f}%)")
    
    if len(sorted_artists) > show_top:
        remaining_artists = len(sorted_artists) - show_top
        remaining_tracks = sum(count for _, count in sorted_artists[show_top:])
        print(f"... 其他 {remaining_artists} 位藝術家: {remaining_tracks} 首")
    
    # 顯示專輯統計 (Top N)
    print(f"\n=== 專輯統計 (Top {show_top}) ===")
    sorted_albums = sorted(album_count.items(), key=lambda x: x[1], reverse=True)
    
    for i, (album, count) in enumerate(sorted_albums[:show_top], 1):
        percentage = (count / len(music_data)) * 100
        print(f"{i:2d}. {album}: {count} 首 ({percentage:.1f}%)")
    
    if len(sorted_albums) > show_top:
        remaining_albums = len(sorted_albums) - show_top
        remaining_album_tracks = sum(count for _, count in sorted_albums[show_top:])
        print(f"... 其他 {remaining_albums} 張專輯: {remaining_album_tracks} 首")
    
    # 總結統計
    print(f"\n=== 總結統計 ===")
    print(f"總藝術家數量: {len(artist_count)}")
    print(f"總專輯數量: {len(album_count)}")
    print(f"平均每位藝術家歌曲數: {len(music_data) / len(artist_count):.1f}")
    print(f"平均每張專輯歌曲數: {len(music_data) / len(album_count):.1f}")
    
    if track_without_artist > 0:
        print(f"缺少藝術家資訊的歌曲: {track_without_artist} 首")
    if track_without_album > 0:
        print(f"缺少專輯資訊的歌曲: {track_without_album} 首")
    
    return artist_count, album_count

def analyze_detailed_info(music_data):
    """分析詳細資訊完整度"""
    print(f"\n=== 資料完整度分析 ===")
    
    complete_info = 0
    has_album_artist = 0
    has_track_info = 0
    empty_entries = 0
    
    for entry_id, entry_data in music_data.items():
        if not entry_data:
            empty_entries += 1
            continue
            
        has_artist = bool(entry_data.get('artist'))
        has_track = bool(entry_data.get('track'))
        has_album = bool(entry_data.get('album'))
        has_album_artist_info = bool(entry_data.get('albumArtist'))
        
        if has_artist and has_track:
            has_track_info += 1
            
        if has_artist and has_track and has_album:
            complete_info += 1
            
        if has_album_artist_info:
            has_album_artist += 1
    
    total_valid = len(music_data) - empty_entries
    
    print(f"有效條目數: {total_valid}")
    print(f"空條目數: {empty_entries}")
    print(f"有基本歌曲資訊 (藝術家+歌名): {has_track_info} 首 ({(has_track_info/total_valid)*100:.1f}%)")
    print(f"有完整資訊 (藝術家+歌名+專輯): {complete_info} 首 ({(complete_info/total_valid)*100:.1f}%)")
    print(f"有專輯藝術家資訊: {has_album_artist} 首 ({(has_album_artist/total_valid)*100:.1f}%)")

def main():
    """主程序"""
    # 從命令行參數或用戶輸入獲取檔案路徑
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    else:
        file_path = input("請輸入JSON檔案路徑: ").strip()
    
    # 獲取顯示數量參數
    show_top = 10
    if len(sys.argv) >= 3:
        try:
            show_top = int(sys.argv[2])
        except ValueError:
            print("警告：無效的顯示數量參數，使用默認值 10")
    
    print("=== 音樂檔案藝術家統計工具 ===")
    print(f"分析檔案: {file_path}")
    print(f"顯示排行: Top {show_top}")
    print("-" * 50)
    
    # 載入檔案
    music_data = load_json_file(file_path)
    if music_data is None:
        return
    
    # 執行分析
    artist_count, album_count = analyze_artists(music_data, show_top)
    analyze_detailed_info(music_data)
    
    print(f"\n分析完成！")
    
    # 詢問是否要保存統計結果
    save_choice = input("\n是否要保存統計結果到檔案？ (y/n): ").strip().lower()
    if save_choice in ['y', 'yes', '是']:
        output_path = input("請輸入輸出檔案路徑 (默認: artist_stats.json): ").strip() or "artist_stats.json"
        
        stats_data = {
            "file_info": {
                "source_file": file_path,
                "total_tracks": len(music_data),
                "total_artists": len(artist_count),
                "total_albums": len(album_count)
            },
            "artist_ranking": [
                {"rank": i+1, "artist": artist, "track_count": count}
                for i, (artist, count) in enumerate(sorted(artist_count.items(), key=lambda x: x[1], reverse=True))
            ],
            "album_ranking": [
                {"rank": i+1, "album": album, "track_count": count}
                for i, (album, count) in enumerate(sorted(album_count.items(), key=lambda x: x[1], reverse=True))
            ]
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            print(f"統計結果已保存至: {output_path}")
        except Exception as e:
            print(f"錯誤：保存統計結果失敗 - {e}")

if __name__ == "__main__":
    # 顯示使用說明
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        print("=== 音樂檔案藝術家統計工具 ===")
        print("使用方法:")
        print("  python analyze_artist_stats.py [JSON檔案] [顯示數量]")
        print("  python analyze_artist_stats.py music.json 15")
        print("  或者直接運行，程式會提示輸入檔案路徑")
        print()
        print("參數說明:")
        print("  JSON檔案   - 要分析的音樂快取JSON檔案")
        print("  顯示數量   - Top N 排行榜數量 (默認: 10)")
        print()
        
        if '--help' not in sys.argv and '-h' not in sys.argv:
            main()
    else:
        main()