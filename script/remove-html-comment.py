import re
import os
import os.path


COMMENT = re.compile(r"""
    <!-- (.*?) -->
""", re.VERBOSE | re.DOTALL)

SCRIPT = re.compile(r"""
    <script (.*?) > ( .*? </script>)?
""", re.VERBOSE | re.DOTALL)

STYLE = re.compile(r"""
    <style (.*?) > (.*?) </style>
""", re.VERBOSE | re.DOTALL)


def clean(data):
    data = COMMENT.sub("", data)
    data = SCRIPT.sub("", data)
    data = STYLE.sub("", data)
    return data
    

def main():
    for filename in os.listdir("raw"):
        rawfile, cleanfile = tuple(os.path.join(p, filename) for p in ("raw", "clean"))
        if os.path.isfile(rawfile):
            print(filename)
            with open(rawfile) as f:
                data = f.read()
            before = len(data)
            data = clean(data)
            after = len(data)
            if before != after:
                print("{0}: {1}".format(filename, before - after))
            with open(cleanfile, "w") as f:
                f.write(data)

if __name__ == '__main__':
    main()
