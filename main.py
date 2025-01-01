import subprocess, os, sys

# Build ffmpeg and ffprobe from source or download at
# https://www.gyan.dev/ffmpeg/builds/
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# only 'bin' folder content needed
# Windows build only

# All tools are suggested to be placed to script folder

contentdir = ''
outdir = ''
createoutdir = True
imagefname = 'image.png'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'

# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def getmediaduration(mp3filename: str):
    global ffprobefname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if mp3filename == '':
        colorprint.out('PATH TO MP3 FILE IS EMPTY')
        return None
    if not os.path.exists(mp3filename):
        colorprint.out('PATH TO MP3 FILE DOES NOT EXIST')
        return None
    subarglist = [ ffprobefname, '-show_entries', 'format=duration','-i',mp3filename ]
    popen  = subprocess.Popen(subarglist, stdout = subprocess.PIPE)
    popen.wait()
    output = str(popen.stdout.read())
    if len(output) > 0 and '\\r\\n' in output:
        return output.split('\\r\\n')[1][9:]
    else:
        return None

def listFilesInFolderByExt(folderpath: str, fileext: str = '.mp3',
                           fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if folderpath == '':
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileext:
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    contentfolder = ''
    outfolder = ''
    inagepath = ''
    outvidfname = ''
    if len(contentdir) == 0 or contentdir is None:
        if len(sys.argv) > 1:
            contentfolder = sys.argv[1]
    else:
        contentfolder = contentdir
    if not os.path.exists(contentfolder):
        colorprint.out('CONTENT FOLDER NOT FOUND')
        systemExitCode = 1
        sys.exit(systemExitCode)
    if len(outdir) == 0:
        if len(sys.argv) > 2:
            outfolder = sys.argv[2]
    else:
        outfolder = outdir
    if len(imagefname) == 0 or imagefname is None:
        if len(sys.argv) > 3:
            imagefname = sys.argv[3]
        else:
            colorprint.out('IMAGE FILENAME NOT SET')
            systemExitCode = 2
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(contentfolder + os.path.sep + imagefname):
            colorprint.out('IMAGE FILENAME DIES NOT EXIST')
            systemExitCode = 3
            sys.exit(systemExitCode)
    imagepath = contentfolder + os.path.sep + imagefname
    if not os.path.exists(outfolder):
        if createoutdir is None:
            if len(sys.argv) > 4:
                createoutdir = sys.argv[4]
                inagepath = contentfolder + os.path.sep + imagefname
            else:
                colorprint.out('OUTPUT FOLDER CREATION PERMISSION NOT SET')
                systemExitCode = 4
                sys.exit(systemExitCode)
        else :
            if createoutdir and not os.path.exists(createoutdir):
                os.makedirs(outfolder)
            else:
                colorprint.out('OUTPUT FOLDER CREATION PERMISSION NOT GRANTED')
                systemExitCode = 5
                sys.exit(systemExitCode)
    scriptdir = get_script_path()
    ffmpegfname = scriptdir + os.path.sep + ffmpegfname
    ffprobefname = scriptdir + os.path.sep + ffprobefname
    if not os.path.exists(ffmpegfname):
        colorprint.out('FFMPEG EXE NOT FOUND')
        systemExitCode = 6
        sys.exit(systemExitCode)
    if not os.path.exists(ffprobefname):
        colorprint.out('FFPROBE EXE NOT FOUND')
        systemExitCode = 7
        sys.exit(systemExitCode)
    filelist = listFilesInFolderByExt(contentfolder, '.mp3', False)
    if filelist is None or len(filelist) == 0:
        colorprint.out('NO FILES FOR CONVERSION FOUND')
        systemExitCode = 8
        sys.exit(systemExitCode)
    convcount = 0
    for file in filelist:
        mp3duration = getmediaduration(contentfolder + os.path.sep + file)
        if mp3duration is None or len(mp3duration) == 0:
            colorprint.out('COULD NOT GET SOUND DURATION')
            systemExitCode = 9
            sys.exit(systemExitCode)
        outvidfname =  outfolder + os.path.sep + file[:-4] + '.mp4'
        if os.path.exists(outvidfname):
            os.remove(outvidfname)
        arglist = [ ffmpegfname ]
        cmdlist = '-loop 1 -framerate 1 -i'.split()
        for el in cmdlist :
            arglist.append(el.strip())
        arglist.append(imagepath)
        arglist.append('-i')
        arglist.append(contentfolder + os.path.sep + file)
        cmdlist = ('-c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -t ' + mp3duration).split()
        for el in cmdlist :
            arglist.append(el.strip())
        arglist.append(outvidfname)
        subprocess.call(arglist, text=True)
        convcount += 1
    print('Done. Converted files (' + str(convcount) + ') are available at ' + outfolder)