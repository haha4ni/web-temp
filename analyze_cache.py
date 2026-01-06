#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音樂快取文件分析工具
分析兩個JSON快取文件，檢測ID重複情況並合併文件
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

def analyze_entry(entry_id, entry_data):
    """分析單個條目的參數"""
    analysis = {
        'id': entry_id,
        'album': entry_data.get('album'),
        'albumArtist': entry_data.get('albumArtist'),
        'artist': entry_data.get('artist'),
        'track': entry_data.get('track'),
        'has_album_info': bool(entry_data.get('album') or entry_data.get('albumArtist')),
        'complete_info': all([
            entry_data.get('artist'),
            entry_data.get('track')
        ])
    }
    return analysis

def compare_entries(entry1, entry2):
    """比較兩個條目是否相同"""
    keys_to_compare = ['album', 'albumArtist', 'artist', 'track']
    for key in keys_to_compare:
        if entry1.get(key) != entry2.get(key):
            return False
    return True

def display_entry_details(entry_data):
    """格式化顯示條目詳情"""
    details = []
    details.append(f"  藝術家: {entry_data.get('artist', 'N/A')}")
    details.append(f"  歌曲名: {entry_data.get('track', 'N/A')}")
    if entry_data.get('album'):
        details.append(f"  專輯: {entry_data.get('album')}")
    if entry_data.get('albumArtist'):
        details.append(f"  專輯藝術家: {entry_data.get('albumArtist')}")
    return '\n'.join(details)

def get_user_choice(conflict_id, entry1, entry2, conflict_num, total_conflicts):
    """讓使用者選擇保留哪個版本"""
    print(f"\n{'='*60}")
    print(f"衝突 {conflict_num}/{total_conflicts}: ID = {conflict_id}")
    print(f"{'='*60}")
    
    print(f"\n【選項1 - 來自 local-cache.json】:")
    print(display_entry_details(entry1))
    
    print(f"\n【選項2 - 來自 local-cache2.json】:")
    print(display_entry_details(entry2))
    
    while True:
        choice = input(f"\n請選擇保留哪個版本 (1/2), 或輸入 's' 跳過此條目, 'q' 退出: ").strip().lower()
        if choice in ['1', '2', 's', 'q']:
            return choice
        print("無效輸入，請輸入 1, 2, s 或 q")

def auto_resolve_remaining_conflicts(conflicts, start_index, default_choice='2'):
    """自動解決剩餘衝突"""
    resolved = {}
    for i in range(start_index, len(conflicts)):
        conflict = conflicts[i]
        if default_choice == '1':
            resolved[conflict['id']] = conflict['file1_data']
        else:
            resolved[conflict['id']] = conflict['file2_data']
    return resolved

def remove_duplicate_ids(merged_cache):
    """移除重複的ID，確保每個ID只出現一次"""
    print(f"\n=== 檢查重複ID ===")
    original_count = len(merged_cache)
    
    # 檢查是否有重複的ID（理論上不應該有，因為dict的key是唯一的）
    id_list = list(merged_cache.keys())
    unique_ids = set(id_list)
    
    if len(id_list) == len(unique_ids):
        print("沒有發現重複的ID")
        return merged_cache
    else:
        # 這種情況在正常情況下不會發生，因為dict的key是唯一的
        print(f"發現異常：ID列表長度 {len(id_list)} 與唯一ID數量 {len(unique_ids)} 不匹配")
        return merged_cache

def analyze_files(file1_path=None, file2_path=None, output_path=None):
    """主要分析函數"""
    # 如果沒有提供參數，則從命令行獲取或使用默認值
    if file1_path is None:
        if len(sys.argv) >= 2:
            file1_path = sys.argv[1]
        else:
            file1_path = input("請輸入檔案１的路徑: ").strip()
    
    if file2_path is None:
        if len(sys.argv) >= 3:
            file2_path = sys.argv[2]
        else:
            file2_path = input("請輸入檔案２的路徑: ").strip()
    
    if output_path is None:
        if len(sys.argv) >= 4:
            output_path = sys.argv[3]
        else:
            output_path = input("請輸入輸出檔案路徑 (默認: out.json): ").strip() or "out.json"
    
    print("=== 音樂快取檔案分析報告 ===")
    print(f"檔案１: {file1_path}")
    print(f"檔案２: {file2_path}")
    print("-" * 50)
    
    # 載入檔案
    cache1 = load_json_file(file1_path)
    cache2 = load_json_file(file2_path)
    
    if cache1 is None or cache2 is None:
        return
    
    # 基礎統計
    print(f"檔案１ 條目數量: {len(cache1)}")
    print(f"檔案２ 條目數量: {len(cache2)}")
    
    # 分析ID重複情況
    ids1 = set(cache1.keys())
    ids2 = set(cache2.keys())
    
    duplicate_ids = ids1 & ids2  # 交集：重複的ID
    unique_to_file1 = ids1 - ids2  # 檔案１獨有的ID
    unique_to_file2 = ids2 - ids1  # 文件2独有的ID
    
    print(f"\n=== ID重复分析 ===")
    print(f"重复ID数量: {len(duplicate_ids)}")
    print(f"文件1独有ID数量: {len(unique_to_file1)}")
    print(f"文件2独有ID数量: {len(unique_to_file2)}")
    
    # 分析重复ID的内容是否相同
    content_conflicts = []
    identical_duplicates = []
    
    for duplicate_id in duplicate_ids:
        entry1 = cache1[duplicate_id]
        entry2 = cache2[duplicate_id]
        
        if compare_entries(entry1, entry2):
            identical_duplicates.append(duplicate_id)
        else:
            content_conflicts.append({
                'id': duplicate_id,
                'file1_data': entry1,
                'file2_data': entry2
            })
    
    print(f"\n=== 重複ID內容分析 ===")
    print(f"內容完全相同的重複ID: {len(identical_duplicates)}")
    print(f"內容有差異的重複ID: {len(content_conflicts)}")
    
    # 顯示內容衝突的詳情
    if content_conflicts:
        print(f"\n=== 內容衝突詳情 ===")
        for i, conflict in enumerate(content_conflicts[:5], 1):  # 只顯示前5個
            print(f"\n衝突 {i}: ID = {conflict['id']}")
            print(f"  文件1: {conflict['file1_data']}")
            print(f"  文件2: {conflict['file2_data']}")
        
        if len(content_conflicts) > 5:
            print(f"... 還有 {len(content_conflicts) - 5} 個衝突未顯示")
    
    # 合併檔案 - 交互式處理衝突
    print(f"\n=== 開始合併過程 ===")
    merged_cache = cache1.copy()  # 從檔案１開始
    
    # 首先添加沒有衝突的條目
    for entry_id in unique_to_file2:
        merged_cache[entry_id] = cache2[entry_id]
    
    # 添加內容相同的重複條目（使用檔案２的版本）
    for duplicate_id in identical_duplicates:
        merged_cache[duplicate_id] = cache2[duplicate_id]
    
    # 交互式處理內容衝突的條目
    skipped_conflicts = []
    user_selections = {}
    
    if content_conflicts:
        print(f"\n發現 {len(content_conflicts)} 個內容衝突，需要您手動選擇...")
        print("提示: 輸入 '1' 選擇第一個版本, '2' 選擇第二個版本")
        print("      輸入 's' 跳過當前衝突, 'q' 退出並自動選擇剩餘項")
        
        for i, conflict in enumerate(content_conflicts):
            choice = get_user_choice(
                conflict['id'], 
                conflict['file1_data'], 
                conflict['file2_data'],
                i + 1,
                len(content_conflicts)
            )
            
            if choice == '1':
                merged_cache[conflict['id']] = conflict['file1_data']
                user_selections[conflict['id']] = 'file1'
            elif choice == '2':
                merged_cache[conflict['id']] = conflict['file2_data']
                user_selections[conflict['id']] = 'file2'
            elif choice == 's':
                skipped_conflicts.append(conflict)
                print(f"已跳过 ID: {conflict['id']}")
            elif choice == 'q':
                print(f"\n使用者選擇退出，剩餘 {len(content_conflicts) - i} 個衝突將自動選擇檔案２版本...")
                remaining_conflicts = content_conflicts[i:]
                auto_resolved = auto_resolve_remaining_conflicts(remaining_conflicts, 0, '2')
                for conflict_id, conflict_data in auto_resolved.items():
                    merged_cache[conflict_id] = conflict_data
                    user_selections[conflict_id] = 'file2_auto'
                break
        
        # 處理跳過的衝突
        if skipped_conflicts:
            print(f"\n=== 處理跳過的 {len(skipped_conflicts)} 個衝突 ===")
            choice = input("對於跳過的衝突，選擇默認行為 (1=選擇檔案１, 2=選擇檔案２, s=真的跳過): ").strip()
            
            if choice == '1':
                for conflict in skipped_conflicts:
                    merged_cache[conflict['id']] = conflict['file1_data']
                    user_selections[conflict['id']] = 'file1_default'
            elif choice == '2':
                for conflict in skipped_conflicts:
                    merged_cache[conflict['id']] = conflict['file2_data']
                    user_selections[conflict['id']] = 'file2_default'
            else:
                print("跳過的衝突將不包含在最終檔案中")
                for conflict in skipped_conflicts:
                    if conflict['id'] in merged_cache:
                        del merged_cache[conflict['id']]
    
    # 检查重复ID
    merged_cache = remove_duplicate_ids(merged_cache)
    
    # 保存合併檔案
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged_cache, f, ensure_ascii=False, separators=(',', ':'))
        print(f"\n=== 合併結果 ===")
        print(f"合併後總條目數: {len(merged_cache)}")
        print(f"追加的新條目數: {len(unique_to_file2)}")
        print(f"合併檔案已保存: {output_path}")
        
        # 顯示使用者選擇統計
        if user_selections:
            print(f"\n=== 使用者選擇統計 ===")
            choice_counts = {}
            for choice in user_selections.values():
                choice_counts[choice] = choice_counts.get(choice, 0) + 1
            
            for choice_type, count in choice_counts.items():
                if choice_type == 'file1':
                    print(f"手動選擇檔案１: {count} 項")
                elif choice_type == 'file2':
                    print(f"手動選擇檔案２: {count} 項")
                elif choice_type == 'file1_default':
                    print(f"默認選擇檔案１: {count} 項")
                elif choice_type == 'file2_default':
                    print(f"默認選擇檔案２: {count} 項")
                elif choice_type == 'file2_auto':
                    print(f"自動選擇檔案２: {count} 項")
        
        if skipped_conflicts:
            print(f"完全跳過的衝突: {len(skipped_conflicts)} 項")
            
    except Exception as e:
        print(f"錯誤：保存合併檔案失敗 - {e}")
    
    # 詳細統計報告
    print(f"\n=== 最終統計報告 ===")
    print(f"原檔案１條目數: {len(cache1)}")
    print(f"原檔案２條目數: {len(cache2)}")
    print(f"重複ID組數: {len(duplicate_ids)}")
    print(f"  - 內容相同的重複: {len(identical_duplicates)}")
    print(f"  - 內容不同的重複: {len(content_conflicts)}")
    print(f"追加的新條目數: {len(unique_to_file2)}")
    print(f"最終合併條目數: {len(merged_cache)}")
    
    # 分析藝術家分佈 (額外分析)
    print(f"\n=== 藝術家統計 (Top 10) ===")
    artist_count = {}
    for entry_data in merged_cache.values():
        artist = entry_data.get('artist', '未知藝術家')
        artist_count[artist] = artist_count.get(artist, 0) + 1
    
    sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
    for i, (artist, count) in enumerate(sorted_artists[:10], 1):
        print(f"{i:2d}. {artist}: {count} 首")
    
    print(f"\n分析完成！合併檔案已保存為: {output_path}")

if __name__ == "__main__":
    # 顯示使用說明
    if len(sys.argv) == 1:
        print("=== 音樂快取檔案分析工具 ===")
        print("使用方法:")
        print("  python analyze_cache.py [檔案１] [檔案２] [輸出檔案]")
        print("  或者直接運行，程式會提示輸入檔案路徑")
        print()
    
    analyze_files()