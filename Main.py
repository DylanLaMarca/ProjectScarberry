values = range(10)
with open('ScarberrySettings') as file:
    count = 0
    for line in file.readlines():
        values[count] = line[line.index('[')+1:line.index(']')]
        count += 1

hertz = values[0]
duty_cycle = values[1]
toggle_count = values[2]
number_of_pictures = values[3]
exposure = values[4]
gain = values[5]
blur_value = values[6]
thresh_limit = values[7]
save_picture = values[8]
feature_image = values[9]