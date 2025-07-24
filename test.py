import os
from nsfw.nsfw_service import setup_nsfw

if __name__ == "__main__":
    # 创建分类器实例
    classifier = setup_nsfw()  # 使用默认模型路径

    # 这里添加指定测试图片目录
    image_dir = 'G:/File/Secret/10010/军事速递/色图/ATFM Tsubaki'

    # 初始化统计列表
    nsfw_files = []      # 色情图片文件名列表 (文件名, result, result2)
    safe_files = []       # 非色情图片文件名列表 (文件名, result, result2)
    near_nsfw_files = []  # 疑似色情图片文件名列表 (文件名, result, result2)

    # 遍历所有文件
    for root, _, files in os.walk(image_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # 跳过非图片文件
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                continue

            try:
                result = classifier.nsfw_risk_ndh(file_path)
                result2 = classifier.nsfw_risk_tf(file_path)

                if result2:  # TF检测为色情
                    nsfw_files.append((file, result, result2))
                elif not result2:
                    if result > 0.6:  # NDH分数>0.6视为色情
                        nsfw_files.append((file, result, result2))
                    elif result > 0.4:  # 0.4-0.6视为疑似
                        near_nsfw_files.append((file, result, result2))
                    else:  # <=0.4视为安全
                        safe_files.append((file, result, result2))

            except Exception as e:
                print(f"[ERROR] Failed to process {file}: {e}")

    # 输出统计结果
    print(f"色情图片总数：{len(nsfw_files)}")
    print("所有色情图片文件名及检测结果：")
    for file_info in nsfw_files:
        print(f"{file_info[0]} | result: {file_info[1]:.5f} | result2: {file_info[2]}")
    
    print(f"\n非色情图片总数：{len(safe_files)}")
    print("所有非色情图片名及检测结果：")
    for file_info in safe_files:
        print(f"{file_info[0]} | result: {file_info[1]:.5f} | result2: {file_info[2]}")
    
    print(f"\n疑似色情图片总数：{len(near_nsfw_files)}")
    print("所有疑似色情图片文件名及检测结果：")
    for file_info in near_nsfw_files:
        print(f"{file_info[0]} | result: {file_info[1]:.5f} | result2: {file_info[2]}")