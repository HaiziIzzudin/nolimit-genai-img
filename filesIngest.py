from raw import convert2raw

from PySide6.QtWidgets import ( QApplication, QFileDialog, QWidget, QVBoxLayout, QTextEdit, )
import os
from datetime import datetime
import pytz
from colorama import Fore, Style
from pymediainfo import MediaInfo
import subprocess


app = QApplication([]) # QApplication must be initialized before QWidget
exiftool_location = r"C:\Program Files\XnViewMP\AddOn"


class filesIngest:
  def select_files(self, kind: str):
    """
    Def for open dialog Select multiple image file
    """
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    if kind == 'images':
      file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.gif *.heic *.heif *.webp)")
      file_dialog.setWindowTitle("Select images to modify its EXIF timestamps")
    elif kind == 'videos':
      file_dialog.setNameFilter("Videos (*.mp4 *.mov *.avi *.mkv)")
      file_dialog.setWindowTitle("Select images to modify its encoding date and other things")

    file_dialog.setDirectory("/")
    

    if file_dialog.exec():
      self.files = file_dialog.selectedFiles()

  
  def getFileList(self):
    """
    Def for get file list
    """
    return self.files
  



  def getFile_EncodedDate(self, filepath, kind):
    
    if kind == 'videos':
      media_info = MediaInfo.parse( convert2raw(filepath) )

      for track in media_info.tracks:
        if track.track_type == 'General':
          datetime_str = track.encoded_date


          # Remove UTC
          datetime_noUTCstr = datetime_str.replace(" UTC", "")
          print('DEBUG: ' + datetime_noUTCstr, end='+++\n')
          # Convert the string to a datetime object
          dtobj_utc = datetime.strptime(datetime_noUTCstr, '%Y-%m-%d %H:%M:%S')


          # Define UTC and MYT timezones
          utc_zone = pytz.utc
          myt_zone = pytz.timezone('Asia/Kuala_Lumpur')
          
          # Localize the datetime object to UTC
          dtobj_utc = utc_zone.localize(dtobj_utc)
          
          # Convert to MYT timezone
          dtobj_myt = dtobj_utc.astimezone(myt_zone)
    
    elif kind == 'images':
      os.chdir(exiftool_location)
      command = [
        './exiftool',
        "-DateTimeOriginal",
        filepath
      ]

      # Run the command and capture the output
      result = subprocess.run(command, capture_output=True, text=True)

      # Find the line with the Date/Time Original information
      output_lines = result.stdout.splitlines()
      # datetime_original_line = None
      for line in output_lines:
          if "Date/Time Original" in line:
              datetime_original_line = line
              break
          
      # Extract the date and time from the line
      _, dts = datetime_original_line.split(": ", 1)
      # The underscore _ is used as a throwaway variable to ignore the first part of the split result (i.e., the label "Date/Time Original"). It's a common Python convention to use _ for variables that are not needed.
      
      # Convert to datetime object
      print(dts)
      dtobj_myt = datetime.strptime(dts, '%Y:%m:%d %H:%M:%S')
      
    return dtobj_myt