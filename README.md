# YouTube Subtitle Downloader

A simple command-line tool to download subtitles/transcripts from YouTube videos.

## Features

- Download subtitles in different languages (defaults to English)
- List all available languages for a video
- Translate subtitles to other languages
- Save subtitles to a file or copy to clipboard
- **Auto-copy to clipboard** when no output file is specified
- Fallback to English or any available language if requested language is not available

## Requirements

- Python 3.6+
- youtube_transcript_api
- pyperclip (for clipboard functionality)

## Installation

1. Make sure you have Python installed
2. Install the required packages:

```bash
pip install youtube_transcript_api pyperclip
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py <youtube_url_or_video_id>
```

Where `<youtube_url_or_video_id>` can be:

- A full YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- A short YouTube URL (e.g., `https://youtu.be/dQw4w9WgXcQ`)
- Just the video ID (e.g., `dQw4w9WgXcQ`)

### Options

- `--language` or `-l`: Specify the language code (default: en)
- `--translate` or `-t`: Translate subtitles to the specified language code
- `--list` or `-ls`: List all available languages for the video
- `--output` or `-o`: Save subtitles to a file (default: copy to clipboard)
- `--clipboard` or `-c`: Copy to clipboard (default when no output file specified)

### Examples

1. Download English subtitles and copy to clipboard (default behavior):

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

2. Download English subtitles using a short YouTube URL (copies to clipboard):

```bash
python main.py https://youtu.be/dQw4w9WgXcQ
```

3. Download English subtitles using just the video ID (copies to clipboard):

```bash
python main.py dQw4w9WgXcQ
```

4. Download Spanish subtitles (copies to clipboard):

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --language es
```

5. List all available languages:

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --list
```

6. Download English subtitles and translate to French (copies to clipboard):

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --language en --translate fr
```

7. Save subtitles to a file (no clipboard):

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output subtitles.txt
```

8. Copy to clipboard AND save to file:

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output subtitles.txt --clipboard
```

9. Explicitly copy to clipboard (same as default behavior):

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --clipboard
```

10. Combine options with file output:

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --language es --translate fr --output french_subtitles.txt
```

11. For URLs with special characters (like `&`), use quotes:

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s"
```

## Language Codes

Some common language codes:

- English: `en`
- Spanish: `es`
- French: `fr`
- German: `de`
- Italian: `it`
- Portuguese: `pt`
- Russian: `ru`
- Japanese: `ja`
- Chinese: `zh`

For a complete list of language codes, use the `--list` option to see what's available for a specific video.

## Clipboard Functionality

**New Feature**: The script now automatically copies transcripts to your clipboard when no output file is specified!

- **Default behavior**: When you run the script without `--output`, the transcript is copied to your clipboard
- **Explicit clipboard**: Use `--clipboard` or `-c` to explicitly copy to clipboard
- **Both clipboard and file**: Use both `--output filename.txt --clipboard` to save to file AND copy to clipboard
- **File only**: Use `--output filename.txt` without `--clipboard` to save only to file (no clipboard)

This makes it super easy to quickly get transcripts and paste them wherever you need them!

## Supported URL Formats

The tool supports various YouTube URL formats:

- Standard YouTube URLs: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short YouTube URLs: `https://youtu.be/VIDEO_ID`
- Mobile YouTube URLs: `https://m.youtube.com/watch?v=VIDEO_ID`
- Embed URLs: `https://www.youtube.com/embed/VIDEO_ID`
- Direct video IDs: `VIDEO_ID`

**Note**: Quotes are only needed in **PowerShell** for URLs containing special characters:

- URLs with `&` (multiple parameters): `"https://www.youtube.com/watch?v=VIDEO_ID&t=30s"`
- URLs with spaces or other special characters

In **bash/Linux/macOS terminals**, quotes are generally not needed. Simple URLs like `https://www.youtube.com/watch?v=VIDEO_ID` work without quotes in all shells.

## Notes

- If the requested language is not available, the script will try to fall back to English
- If English is not available, it will try to get any available language
- Not all videos have subtitles available
- Translation is only available for certain languages and depends on YouTube's capabilities
