"""code2yaml.py

Convert contents of `scripts` directory to YAML.

"""
import os
import black


def code2yaml():
    """Convert contents of `scripts` directory to YAML.

    """

    for i, f in enumerate(os.listdir(os.getcwd())):

        src = os.path.join(os.getcwd(), f)
        contents = open(src).read()
        kwargs = {"fast": True, "mode": black.FileMode()}
        _, ext = os.path.splitext(f)
        if ext == ".py":
            try:
                # for some reason I can't get "in-place" formatter to work, so I just
                # overwrite the file instead
                contents = black.format_file_contents(contents, **kwargs)
            except black.NothingChanged:
                pass
        open(src, "w").write(contents)
        contents = "  " + contents.replace("\n", "\n  ").rstrip() + "\n"
        contents = f"{f.replace('.', '__')}: |\n" + contents
        open("../../_data/code.yaml", "w" if i == 0 else "a").write(contents)


if __name__ == "__main__":
    code2yaml()
