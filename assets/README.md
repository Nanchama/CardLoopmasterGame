# Chronoloop approved PWA icons

This directory contains the exact approved app-icon artwork.
The 192px PNG is kept as a binary file.
The 512px PNG is stored as nine Base64 text parts because of a binary-transfer limitation.
`scripts/build.py` concatenates/decodes these parts and validates SHA-256 so the emitted
`dist/icon-512.png` is byte-for-byte identical to the approved 512px PNG.

Do not replace these assets with programmatically redrawn art.
