# videocreator
Script creates MP4 files from MP3 files and an image (PNG preferred)

Script uses fffmpeg / ffprobe exe tools, read more on this in script comments

Tested with Windows 10

Can be called with arguments:
| Ppsition | Suggested type | Description |
| --- | --- | --- |
| 1 | String | Path to folder containing MP3 files and image
| 2 | String | Path to folder containing ourput files |
| 3 | Boolean | If true, script creates output folder

Script return codes:
| Code | Description |
| --- | --- |
| 0 | Successful execution |
| 1 | Content folder not found |
| 2 | Image filename not found |
| 3 | Image filename does not exist |
| 4 | Output folder creation permisssion not set |
| 5 | Output folder creation permisssion not granted |
| 6 | ffmpeg exe not found |
| 7 | ffprobe exe not found |
| 8 | No files for conversion found |
| 9 | Could not get sound duration |
