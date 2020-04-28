#!/usr/bin/env python3

import argparse
from pathlib import Path

from colorama import init, Fore, Style

from .elf import ELFSecurity, RelroType


def parse_args() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to be analyzed")
    args = parser.parse_args()
    filepath = Path(args.file)
    if not filepath.exists():
        raise RuntimeError(f"file {filepath} does not exists")
    return filepath


def main():
    filepath = parse_args()
    checksec = ELFSecurity(filepath)
    init()
    # display results
    relro = checksec.has_relro
    if relro == RelroType.No:
        print(f"RELRO: {Fore.RED}{checksec.has_relro.name}{Style.RESET_ALL}")
    else:
        print(f"RELRO: {Fore.GREEN}{checksec.has_relro.name}{Style.RESET_ALL}")

    if not checksec.has_canary:
        print(f"Canary: {Fore.RED}No{Style.RESET_ALL}")
    else:
        print(f"Canary: {Fore.GREEN}Yes{Style.RESET_ALL}")

    if not checksec.has_nx:
        print(f"NX: {Fore.RED}No{Style.RESET_ALL}")
    else:
        print(f"NX: {Fore.GREEN}Yes{Style.RESET_ALL}")

    if not checksec.is_pie:
        print(f"PIE: {Fore.RED}No{Style.RESET_ALL}")
    else:
        print(f"PIE: {Fore.GREEN}Yes{Style.RESET_ALL}")

    if checksec.has_rpath:
        print(f"RPATH: {Fore.RED}Yes{Style.RESET_ALL}")
    else:
        print(f"RPATH: {Fore.GREEN}No{Style.RESET_ALL}")

    if checksec.has_rpath:
        print(f"RUNPATH: {Fore.RED}Yes{Style.RESET_ALL}")
    else:
        print(f"RUNPATH: {Fore.GREEN}No{Style.RESET_ALL}")

    if not checksec.is_stripped:
        print(f"Symbols: {Fore.RED}Yes{Style.RESET_ALL}")
    else:
        print(f"Symbols: {Fore.GREEN}No{Style.RESET_ALL}")

    fortified_funcs = checksec.fortified
    if not fortified_funcs:
        print(f"Fortified: {Fore.RED}No{Style.RESET_ALL}")
    else:
        print(f"Fortified: {Fore.GREEN}{len(fortified_funcs)}{Style.RESET_ALL}")

    fortifiable_funcs = checksec.fortifiable
    if not fortifiable_funcs:
        print(f"Fortifiable: {Fore.RED}No{Style.RESET_ALL}")
    else:
        print(f"Fortifiable: {Fore.GREEN}{len(fortifiable_funcs)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
