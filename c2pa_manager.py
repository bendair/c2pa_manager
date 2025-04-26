#!/usr/bin/env python3
"""
c2pa_manager.py

A command-line utility to create, embed, inspect, and verify C2PA manifests in media files using the c2pa-python SDK.
"""
import argparse
import sys
import os
from c2pa import manifest_builder, receipt


def embed_manifest(input_path, output_path, key_path, cert_paths, publisher, software):
    # Read input file
    with open(input_path, 'rb') as f:
        data = f.read()

    # Build the manifest
    builder = manifest_builder.ManifestBuilder()
    if publisher:
        builder.set_publisher(publisher)
    if software:
        # software should be provided as "Name:Version"
        name, version = software.split(":", 1)
        builder.add_software(name, version)

    # Sign the manifest
    with open(key_path, 'rb') as kf:
        private_key = kf.read()
    cert_chain = []
    for cert in cert_paths:
        with open(cert, 'rb') as cf:
            cert_chain.append(cf.read())

    builder.sign(private_key=private_key, certificate_chain=cert_chain)

    # Embed into file
    mime = _guess_mime(input_path)
    out_bytes = builder.embed(data, mime)
    with open(output_path, 'wb') as outf:
        outf.write(out_bytes)

    print(f"✅ Embedded C2PA manifest into '{output_path}'")


def verify_manifest(input_path):
    # Verify the manifest and print status
    rcpt = receipt.Receipt.from_file(input_path)
    result = rcpt.verify()
    print(f"▶ Verification status: {result.status}")
    # Optionally print full manifest
    print("\nManifest assertions:")
    print(rcpt.manifest)


def show_manifest(input_path):
    # Extract and display manifest JSON
    rcpt = receipt.Receipt.from_file(input_path)
    print(rcpt.manifest.to_json(indent=2))


def _guess_mime(path):
    ext = os.path.splitext(path)[1].lower()
    return {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.pdf': 'application/pdf',
    }.get(ext, 'application/octet-stream')


def main():
    parser = argparse.ArgumentParser(description="Create and manage C2PA manifests.")
    sub = parser.add_subparsers(dest='command', required=True)

    # Embed command
    e = sub.add_parser('embed', help='Embed a new manifest into a file')
    e.add_argument('--input', '-i', required=True, help='Input file path')
    e.add_argument('--output', '-o', required=True, help='Output file path')
    e.add_argument('--key', required=True, help='Path to private key PEM')
    e.add_argument('--cert', required=True, nargs='+', help='Certificate chain PEM(s)')
    e.add_argument('--publisher', help='Publisher name')
    e.add_argument('--software', help='Software in format Name:Version')

    # Verify command
    v = sub.add_parser('verify', help='Verify a file with embedded manifest')
    v.add_argument('--input', '-i', required=True, help='File to verify')

    # Show manifest
    s = sub.add_parser('show', help='Print extracted manifest JSON')
    s.add_argument('--input', '-i', required=True, help='File to inspect')

    args = parser.parse_args()

    if args.command == 'embed':
        embed_manifest(args.input, args.output, args.key, args.cert, args.publisher, args.software)
    elif args.command == 'verify':
        verify_manifest(args.input)
    elif args.command == 'show':
        show_manifest(args.input)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
