#!/bin/bash

# Configuration
REMOTE_NAME="gdrive"
REMOTE_PATH="website/rogue_bachata_website"

echo "Starting 2-way SAFE sync (No files will be deleted)..."

# 1. Download from Drive -> Local
# 'copy' only adds new/changed files. It NEVER deletes local files.
echo "Downloading new images from Google Drive..."
~/.local/bin/rclone copy "$REMOTE_NAME:$REMOTE_PATH/images" images/ --verbose

echo "Downloading new videos from Google Drive..."
~/.local/bin/rclone copy "$REMOTE_NAME:$REMOTE_PATH/videos" videos/ --verbose

# 2. Upload from Local -> Drive
# 'copy' only adds new/changed files to Drive. It NEVER deletes Drive files.
echo "Uploading local images to Google Drive..."
~/.local/bin/rclone copy images/ "$REMOTE_NAME:$REMOTE_PATH/images" --verbose

echo "Uploading local videos to Google Drive..."
~/.local/bin/rclone copy videos/ "$REMOTE_NAME:$REMOTE_PATH/videos" --verbose

echo "Sync complete! Local and Remote folders are now consistent."