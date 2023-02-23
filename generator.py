import pandas as pd
from PIL import Image
import cv2
import extcolors
import easydev
from colormap import rgb2hex


# function to convert the list output by extcolors into a pandas dataframe
def colour_to_df(input_colours):
    colours_list = str(input_colours).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colours_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colours_list]

    df_colour_hex = [
        rgb2hex(int(i.split(', ')[0].replace('(', '')),
                int(i.split(', ')[1]),
                int(i.split(', ')[2].replace(')', ''))) for i in df_rgb]

    df = pd.DataFrame(zip(df_colour_hex, df_percent), columns=['hex_code', 'occurrence'])
    return df


# function to produce a list of hex_colours and a resized image for faster processing
def produce_list(input_name, input_file_path, resize_folder):
    # resize and save the image
    output_width = 900
    img = Image.open(input_file_path)
    wpercent = (output_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((output_width, hsize), Image.ANTIALIAS)
    resize_name = 'resize_' + input_name
    img.save(f"{resize_folder}/{resize_name}")
    img_url = f"{resize_folder}/{resize_name}"

    # extract 10 most prevalent colours from image using extcolors and return a list of hex codes
    colours = extcolors.extract_from_path(img_url, tolerance=11, limit=11)
    df_colour = colour_to_df(colours)
    hex_list = list(df_colour['hex_code'])
    return hex_list, img_url
