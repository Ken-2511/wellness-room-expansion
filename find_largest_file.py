import os

def find_largest_file(directory):
    largest_file = None
    largest_size = 0

    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                # Update largest file if current one is larger
                if file_size > largest_size:
                    largest_size = file_size
                    largest_file = file_path
            except OSError as e:
                print(f"Error accessing file {file_path}: {e}")

    return largest_file, largest_size

if __name__ == "__main__":
    directory = input("请输入要查找的目录路径：")
    largest_file, largest_size = find_largest_file(directory)
    if largest_file:
        print(f"目录中最大的文件是: {largest_file}")
        print(f"文件大小为: {largest_size / (1024 * 1024):.2f} MB")
    else:
        print("未找到文件或目录无访问权限。")
