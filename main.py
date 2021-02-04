import getopt
import sys
import PIL.Image

ascii_chars = ['@', '#', '$', '%', '&', '?',
               '*', '+', '-', ';', ':', "'", ',', '.']


def resize(image, new_w=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_h = int(ratio * new_w)
    resized_image = image.resize((new_w, new_h))
    return resized_image


def grey_scale(image):
    grey_image = image.convert('L')
    return grey_image


def pixel_to_ascii(image):
    pixels = image.getdata()
    chars = "".join(ascii_chars[pixel//22] for pixel in pixels)
    return chars


def transform_image(image, new_w=100):
    new_image_data = pixel_to_ascii(grey_scale(resize(image)))
    pixel_count = len(new_image_data)
    new_image = "\n".join(new_image_data[i:i+new_w]
                          for i in range(0, pixel_count, new_w))
    return new_image


def main():
    short_options = "hf:"
    long_options = ["help", "file="]
    path = ""
    try:
        argument_list = sys.argv[1:]
        arguments, values = getopt.getopt(
            argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
    for arg, val in arguments:
        if arg in ("-h", "--help"):
            str = "commands:\n 1. -h or --help \n 2. -f <image_path> or --file <image_path>"
            print(str)
            sys.exit(2)
        elif arg in ("-f", "--file"):
            path = val

    print('Image path:', path)
    try:
        image = PIL.Image.open(path)
        new_image = transform_image(image)
        name = (path.split("/")[-1]).split(".")[0]
        with open('ascii_images/' + name + '.txt', 'w') as f:
            f.write(new_image)
    except Exception as e:
        print(path, e)


main()
