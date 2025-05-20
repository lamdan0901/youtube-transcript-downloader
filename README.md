# YouTube Subtitle Downloader

A simple command-line tool to download subtitles/transcripts from YouTube videos.

## Features

- Download subtitles in different languages (defaults to English)
- List all available languages for a video
- Translate subtitles to other languages
- Save subtitles to a file
- Fallback to English or any available language if requested language is not available

## Requirements

- Python 3.6+
- youtube_transcript_api

## Installation

1. Make sure you have Python installed
2. Install the required package:

```bash
pip install youtube_transcript_api
```

## Usage

### Basic Usage

```bash
python youtube_downloader\main.py <video_id>
```

Where `<video_id>` is the YouTube video ID (the part after `v=` in the YouTube URL).

### Options

- `--language` or `-l`: Specify the language code (default: en)
- `--translate` or `-t`: Translate subtitles to the specified language code
- `--list` or `-ls`: List all available languages for the video
- `--output` or `-o`: Save subtitles to a file (default: video_id_language.txt)

### Examples

1. Download English subtitles for a video:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ
```

2. Download Spanish subtitles:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ --language es
```

3. List all available languages:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ --list
```

4. Download English subtitles and translate to French:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ --language en --translate fr
```

5. Save subtitles to a file:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ --output subtitles.txt
```

6. Combine options:
```bash
python youtube_downloader\main.py dQw4w9WgXcQ --language es --translate fr --output french_subtitles.txt
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

## Notes

- If the requested language is not available, the script will try to fall back to English
- If English is not available, it will try to get any available language
- Not all videos have subtitles available
- Translation is only available for certain languages and depends on YouTube's capabilities
