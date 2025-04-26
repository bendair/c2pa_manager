c2pa_manager.py

A standalone Python CLI script using the official c2pa-python SDK. It lets you:

embed a new manifest (with publisher/software assertions)

verify an existing provenance chain

show the full manifest JSON

All you need is your PEM-encoded signing key and certificate chain. Let me know if you’d like to add extra assertion types (geo, ingredients, etc.) or integrate with a key management service!

A command-line utility to create, embed, inspect, and verify C2PA manifests in media files using the c2pa-python SDK.

Supports
'.jpg': 'image/jpeg',
'.jpeg': 'image/jpeg',
'.png': 'image/png',
'.mp4': 'video/mp4',
'.mov': 'video/quicktime',
'.pdf': 'application/pdf',

Example
# Embed provenance into a JPEG
python c2pa_manager.py embed \
  --input   photo.jpg \
  --output  photo_prov.jpg \
  --key      mykey.pem \
  --cert     cert1.pem cert2.pem \
  --publisher "Acme Studio" \
  --software "AcmeEditor:3.4.1"

# Verify the provenance you just embedded
python c2pa_manager.py verify \
  --input photo_prov.jpg

▶ Verification status: AllChecksPass

Manifest assertions:
Manifest(
  publisher="Acme Studio",
  software=[Software(name="AcmeEditor", version="3.4.1")],
  ingredients=[ ... ],
  timestamps={ created: "2025-04-26T14:03:22Z" },
  ...
)

Example 2) Show full manifest JSON

# Dump the raw manifest JSON for inspection
python c2pa_manager.py show \
  --input photo_prov.jpg

Sample Output:
{
  "@context": "https://w3id.org/security/v2",
  "type": "Claim",
  "publisher": "Acme Studio",
  "software": [
    {
      "name": "AcmeEditor",
      "version": "3.4.1"
    }
  ],
  "ingredients": [
    {
      "name": "photo.jpg#0",
      "hash": "sha256:abc123..."
    }
  ],
  "manifestHash": "sha256:def456...",
  "signature": {
    "type": "RsaSignature2018",
    "creator": "did:example:123#key-1",
    "signatureValue": "XyZ..."
  }
}

Feel free to swap in video (.mp4), PDF or other file types—the script auto-guesses MIME based on file extension. Let me know if you need examples for more advanced assertions (geo-tags, cloud storage bindings, custom claims, etc.).
