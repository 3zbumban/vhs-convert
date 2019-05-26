#!/usr/bin/env python3
from subprocess import Popen, PIPE, STDOUT
import json
import argparse
import subprocess

MY_VI_DEVICE = "USB2.0 Grabber"
MY_AU_DEVICE = "Digitale Audioschnittstelle (USB Audio Interface)"
V_CH = "0"
A_CH = "4"

e_dict = {
  "E-30": "01:05:00",
  "E-60": "02:07:00",
  "E-90": "03:07:00",
  "E-120": "04:09:00",
  "E-150": "05:09:00",
  "E-180": "06:10:00",
  "E-195": "06:38:00",
  "E-200": "06:46:00",
  "E-210": "07:14:00",
  "E-240": "08:17:00",
  "E-270": "09:20:00",
  "E-300": "10:21:00"
}

parser = argparse.ArgumentParser(description='Video Capture')
parser.add_argument("--video_size", default="720x480", help='Video resolution setting for capture device')
parser.add_argument("--scale_to", default="640x480", help='Scale video to resolution')
parser.add_argument("--fps", default=29.97, type=float, help='Frames per second (float)')
parser.add_argument("--device", default=MY_VI_DEVICE, help='Capture device name')
parser.add_argument("--time", default="6:10:00", help='Capture time limit')
parser.add_argument("--crf", default=24, type=int, help='CRF setting')
parser.add_argument("--maxrate", default=25000, type=int, help='Maximum bitrate')
parser.add_argument("--out", required=True, help='Output file')
parser.add_argument("--preset", default="fast", help="ffmpeg capture preset `veryslow`, `slower`, `slow`, `medium`, `fast`, `faster`, `veryfast`.")
parser.add_argument("--shutdown", required=False, help="add flag to shudown after finisch..", default=False, action="store_true")

args, unkown = parser.parse_known_args()

def shutdown():
  print("shutting down in 120sec..")
  subprocess.call(["shutdown", "/s", "/t", "120"])

def e_to_time(s):
  return e_dict[s]

# rotes audio kebel hernehmen!

# convert E-** to time **:**:** https://en.wikipedia.org/wiki/VHS "PAL market"
if args.time.startswith("E"):
  if args.time in e_dict.keys():
    print("convert E-** to timeformat...")
    args.time = e_to_time(args.time)

cmd = [
  "ffmpeg",
  "-framerate", str(args.fps), 
  "-vsync", "1", 
  "-video_size", "720x480",
  "-f", "dshow",
  "-rtbufsize", "450000k",
  "-crossbar_video_input_pin_number", V_CH, # video pin
  "-crossbar_audio_input_pin_number", A_CH, # audio pin
  "-i", "video=" + MY_VI_DEVICE + ":audio=" + MY_AU_DEVICE, # MY_AU_DEVICE
  "-t", args.time,
  "-force_key_frames", ",".join(["00:00:%02d.000" % x for x in range(11)]),
  "-vf", "fps=" + str(args.fps) + ",yadif=0:0:0,hqdn3d=6:4:6:4,scale=" + args.scale_to,
  "-c:v", "libx264",
  "-preset", args.preset,
  "-tune", "film", 
  "-profile:v", "main", 
  "-level", "3.1",
  "-pix_fmt", "yuv420p",
  "-crf", str(args.crf),
  "-maxrate", str(args.maxrate) + "k",
  "-bufsize", str(args.maxrate*2) + "k",
  "-af", "aresample=async=1000,highpass=200,lowpass=3500",
  "-c:a", "aac",
  "-b:a", "96k",
  "-strict", "-2",
  "-r", str(args.fps),
  args.out
]

def main():
  input("Start? \n\n\n")
  try:
    print("".join(cmd) + "\n\n\n\n\n\n")
    p = Popen(cmd, stdout=None, stderr=None)
    exit = p.wait()
    print("FFMPEG exit code " + str(exit))
    # from subprocess import Popen, PIPE, STDOUT
    # p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
    # grep_stdout = p.communicate(input=b'one\ntwo\nthree\nfour\nfive\nsix\n')[0]
    # print(grep_stdout.decode())
    # # -> four
    # # -> five
    # # ->
    if args.shutdown:
      shutdown()
    else:
      pass
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  main()