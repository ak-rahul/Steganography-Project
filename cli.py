# cli.py
import argparse
from core.stego import hide_text, extract_text
import os

def cmd_embed(args):
    out = args.output if args.output else None
    if not out:
        base = os.path.basename(args.input)
        out = os.path.join(os.getcwd(), f"stego_{base}")
    saved = hide_text(args.input, args.message, args.password, output_path=out)
    print(f"Saved: {saved}")

def cmd_extract(args):
    text, used_struct = extract_text(args.input, args.password if args.password else None)
    print("---- Decrypted message ----")
    print(text)

def main():
    p = argparse.ArgumentParser(description="SteganoX CLI")
    sub = p.add_subparsers(dest="cmd")

    e = sub.add_parser("embed")
    e.add_argument("--input", "-i", required=True)
    e.add_argument("--message", "-m", required=True)
    e.add_argument("--password", "-p", default=None)
    e.add_argument("--output", "-o", default=None)

    d = sub.add_parser("extract")
    d.add_argument("--input", "-i", required=True)
    d.add_argument("--password", "-p", default=None)

    args = p.parse_args()
    if args.cmd == "embed":
        cmd_embed(args)
    elif args.cmd == "extract":
        cmd_extract(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
