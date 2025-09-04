def split_file(file_path, part_size):
    file_name = file_path.split('/')[-1]
    part_num = 0
    with open(file_path, 'rb') as file:
        chunk = file.read(part_size)
        while chunk:
            part_num += 1
            part_file_path = f"{file_name}.part{part_num}"
            with open(part_file_path, 'wb') as part_file:
                part_file.write(chunk)
            chunk = file.read(part_size)

    print(f"File split into {part_num} parts.")


file_path = "./models/02-acuracia-79_03-ENet.h5"
part_size = 90 * 1024 * 1024  # 100 MB
split_file(file_path, part_size)
