"""
Method generate_subitles generates subtitle file in .srt format. 
Takes argument:
tagging_data <dict> with fields:
{   
    'idx'
    'text'
    'start_time'
    'end_time'
}
"""

import os

def format_milliseconds(milliseconds):
    total_seconds = int(milliseconds // 1000)
    ms = int(milliseconds % 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def generate_subitles(tagging_data, output_file_name, output_dir = "."):

    output_file_name = output_file_name + ".srt"
    output_file_path = os.path.join(output_dir,output_file_name)

    with open(output_file_path, 'w') as subtitles_file:
        for idx in range(len(tagging_data)):
            
            start_time_str = format_milliseconds(tagging_data[idx]['start_time'])
            end_time_str = format_milliseconds(tagging_data[idx]['end_time'])

            subtitles_file.write(f"{idx}\n")
            subtitles_file.write(f"{start_time_str} --> {end_time_str}\n")
            subtitles_file.write(f"{tagging_data[idx]['text']}\n\n")

    print(f"Succesfully created .srt subtitle file {output_file_path}")
    return output_file_path