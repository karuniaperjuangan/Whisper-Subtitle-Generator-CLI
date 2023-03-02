import whisper
import datetime
import re
import os

#OpenAI Whisper CLI for Subtitle Generation
import argparse
parser = argparse.ArgumentParser(
    prog="whispersub",
    description="OpenAI Whisper CLI for Subtitle Generation",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("input_file", type=str, help="Input file")
parser.add_argument("input_folder", type=str, help="Input folder")
parser.add_argument("-m","--model", type=str, default="base", help="Model name")
parser.add_argument("--output_language", type=str, help="Output language")
parser.add_argument("--no_timestamps", action="store_true", help="Do not output timestamps")

args = parser.parse_args()

model = whisper.load_model(args.model)
def generate_subtitle(filename):
    result = model.transcribe(filename)

    srt_string = ""

    no_timestamp_string = ""

    for index,part in enumerate(result['segments']):
        srt_string += f'{index+1}\n'
        srt_string += f'{datetime.timedelta(seconds=int(part.get("start",0)))} --> {datetime.timedelta(seconds=int(part.get("end",0)))}\n'
        srt_string += f'{part.get("text","").lstrip()}\n\n'
        no_timestamp_string += f'{part.get("text","").lstrip()}\n'
    
    if args.no_timestamps:
        with open('.'.join(filename.split('.')[:-1])+"_NO_TIMESTAMP.txt",'w') as f:
            f.write(no_timestamp_string)
    else:
        with open('.'.join(filename.split('.')[:-1])+".srt",'w') as f:
            f.write(srt_string)
    
    
    print("Subtitle file generated for",filename)
    
    return result

def main():   
    supported_formats = ['mp4','mkv','avi','mov','flv','wmv','webm','mpg','mpeg','m4v','3gp','3g2','f4v','f4p','f4a','f4b']
    if args.input_folder:
        for item in os.listdir(args.input_folder):
            if re.search('|'.join(supported_formats),item):
                try:
                    print("Transcribing",item)
                    generate_subtitle(os.path.join(args.input_folder,item))
                except Exception as e:
                    print("Error while transcribing",item)
                    print(f"Reason: {e}")
    if args.input_file:
        
        generate_subtitle(args.input_file)
