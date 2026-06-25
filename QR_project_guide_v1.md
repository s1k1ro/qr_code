# QR Code Generator: Project Guide

Your first self-directed Python project. A command-line tool that turns input into QR codes, built on the `qrcode` library, with enough of your own code around it that it is a real project and not a thin wrapper.

## The real goal

You already know how to read Python. The thing you are building here is the ability to compose it from an empty file. That skill only comes from doing it while it feels uncomfortable. The QR tool is the vehicle. By the end you also get a portfolio piece worth showing.

## The one rule

For this project, you write every line yourself.

Use AI (me, Claude Code, anything) as a tutor, a code reviewer, a debugger, and a source of "what is the general approach here." Paste your own broken code and ask why it breaks. Ask what a concept means. Ask which library class to look up.

Do not ask anyone to write the function for you. The moment you paste in a finished implementation, the skill you came for evaporates. That is the line. Hold it.

## Environment

You are set up: WSL (Ubuntu), a virtual environment, VS Code connected into WSL, project at `~/projects/qr_code`.

Every time you sit down to work, run these two first:

```
cd ~/projects/qr_code
source venv/bin/activate
```

You know it worked when your prompt shows the `(venv)` prefix. If you forget this and `pip` or your imports act strange, the venv is almost always not active.

Keep the project inside the Linux home, not under `/mnt/c`. Roblox, Ableton, and Kdenlive stay on Windows. Python and boot.dev live here in WSL. They do not share an environment.

## Git discipline

You already do commit-per-step on The Last Slice. Same habit here. Commit after every version below that works, with a short message. Push to GitHub under s1k1ro. By v7 the repo itself is part of the deliverable.

```
git init
git add .
git commit -m "v1: read data from a command-line argument"
```

## The build ladder

Each step adds one thing and stays runnable. Never write more than ten to fifteen lines without running the program. Do not skip ahead.

### v0: prove the pipeline (DONE)
- Goal: confirm the library and environment work.
- Build: import `qrcode`, make a code from a hardcoded string, save the PNG.
- Done when: you scan the png with your phone. Achieved.

### v1: read input from the command line
- Goal: stop hardcoding the data.
- Build: use `argparse` to take the data string as an argument, so `python qr.py "hello"` works.
- Learn: argparse basics, reading arguments into your program.
- Research: the `argparse` standard library docs, the "ArgumentParser" and "add_argument" sections.
- Done when: changing the command-line text changes the QR, with no code edits.
- Time: 1 to 2 hours.

### v2: output path and graceful failure
- Goal: control where the file goes and stop ugly crashes.
- Build: add an optional output-path argument with a sensible default. Handle the case where no data is given by printing a clear message instead of a traceback.
- Learn: optional arguments, default values, simple input validation.
- Done when: `python qr.py "hi" -o mycode.png` saves to that name, and running with no data prints a friendly message.
- Time: 1 to 2 hours.

### v3: the knobs (including your first colour customiser)
- Goal: expose real options.
- Build: arguments for box size, border, error-correction level (the L, M, Q, H choices), and foreground and background colour.
- Note: `qrcode.make()` is too simple for this. You will need to graduate to the `qrcode.QRCode(...)` object, add your data to it, then call `make_image` with the colour and error-correction settings. This is a real step up and where you learn the library properly.
- Learn: mapping CLI flags to function parameters, restricted choices in argparse, the QRCode object.
- Research: the `qrcode` README "Advanced Usage" section, the four `ERROR_CORRECT_*` constants, and the `fill_color` and `back_color` options.
- Done when: you can generate a blue-on-white code at high error correction from the command line.
- Time: 2 to 4 hours.

### v4: refactor into functions (the composition lesson)
- Goal: same behaviour, better shape.
- Build: split the one big block into small functions, for example `parse_args()`, `build_qr(data, options)`, `save_qr(img, path)`, and a thin `main()` that calls them in order.
- Learn: decomposition. This is the exact skill the whole project is for. Doing it on code that already works is the safe way to practise it.
- Done when: the tool behaves identically but each function does one clear job.
- Time: 2 to 3 hours.

### v5: input types
- Goal: do something the thousand toy versions do not.
- Build: a `--type` flag with options text, url, wifi, and vcard. Each type is a small function that returns the string to encode. Text is the raw input. URL validates it looks like a link. WiFi and vCard build a specific formatted string from extra arguments (ssid, password, name, etc).
- Learn: branching or dispatch, string templating, more functions.
- Research: the WiFi and vCard string formats (reference formats are in the appendix below). You write the functions that build them.
- Done when: a wifi-type code, when scanned, offers to join the network.
- Time: 3 to 5 hours.

### v6: batch mode
- Goal: generate many codes at once.
- Build: a `--batch input.csv` option that reads rows and produces one QR per row, named from a column.
- Learn: file input and output, the `csv` standard library module, loops, and handling one bad row without killing the whole run.
- Done when: a CSV of ten rows produces ten correctly named PNGs.
- Time: 3 to 5 hours.

### v7: make it a portfolio piece (boot.dev requirement met here)
- Goal: turn a script into something you can show.
- Build: a README explaining what the tool is, how to clone it, and how to run it, with a screenshot. A `requirements.txt`. A few `pytest` tests. A clean GitHub repo.
- Learn: testing, basic packaging, documentation.
- Test tip: test the pure formatter functions from v5. Given known WiFi inputs, assert the exact output string. Pure functions are the easiest things to test.
- Done when: a stranger could clone your repo and run it from the README alone. At this point boot.dev's requirements are satisfied and the project is portfolio-ready.
- Time: 3 to 5 hours.

### v8: the shareable version
- Goal: the screenshot that makes people on Reddit go "oh, how".
- Build: a logo embedded in the centre, rounded modules, colour gradients, and SVG output.
- Learn: more of the library's image styling, image composition.
- Research: in the `qrcode` "Advanced Usage" docs, look up `StyledPilImage`, the module drawers (rounded modules and others), the colour masks (gradients), the logo embed option, and the SVG image factories. Wire them into the same `build_qr` you already have.
- Done when: you generate a styled code with your logo that still scans reliably.
- Time: 4 to 8 hours.

### v9: optional stretch, the from-scratch encoder
- Goal: the algorithmic deep dive, only if you want it.
- Build: replace the library inside `build_qr` with your own QR encoder, keeping the interface identical so the tool never stops working.
- Research: Thonky's QR Code Tutorial, and Nayuki's reference implementation for sanity-checking. The wall is Reed-Solomon error correction over a Galois field. Start with byte mode, a few versions, and one error-correction level.
- Time: 20 to 40 hours. This is a separate project on top, not counted in the estimate below.

## Time and milestones

- v0: done, about 15 minutes.
- v1: 1 to 2 hours.
- v2: 1 to 2 hours.
- v3: 2 to 4 hours.
- v4: 2 to 3 hours.
- v5: 3 to 5 hours.
- v6: 3 to 5 hours.
- v7: 3 to 5 hours.
- v8: 4 to 8 hours.

Through v7 (portfolio-complete, boot.dev satisfied): roughly 15 to 25 focused hours.
Through v8 (worth posting): roughly 20 to 35 focused hours.
At a couple of nights a week, expect a month or two of calendar time. The error bars are wide because you are learning, which is exactly the point.

## How to get unstuck

- Always keep a running program. Small loop, constant feedback.
- When you do not know how to structure something, write the steps as plain-English comments first, then translate each comment into one line of code. The comments are you thinking in words you already have.
- Read the last line of a traceback first. It usually names the actual problem.
- If something works, commit before you change it.
- Stuck for more than twenty minutes on the same wall? That is when you bring it to me, with your code and the error pasted in.

## Definition of done

The project is done at v7. v8 is the version worth sharing. v9 is for if you caught the bug and want the algorithmic challenge.

## Appendix: reference formats

These are target string formats for v5. You write the functions that build them from arguments.

WiFi:
```
WIFI:S:<ssid>;T:WPA;P:<password>;;
```

vCard (minimal):
```
BEGIN:VCARD
VERSION:3.0
N:<lastname>;<firstname>
FN:<full name>
TEL:<phone>
EMAIL:<email>
END:VCARD
```