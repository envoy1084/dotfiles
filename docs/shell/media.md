# Media, images and Markdown

[← Previous: Networking and cloud files](networking.md) · [Docs index](../index.md) · [Next: System overview →](system.md)

Use `tools image`, `tools video` or `tools audio` to find parameterised recipes. The FFmpeg recipes use `-n` to stop instead of overwriting an existing output.

### FFmpeg

[Project / documentation](https://ffmpeg.org/) · Homebrew: `ffmpeg`.

Inspect, convert, trim, and extract audio/video; includes ffprobe.

```sh
ffprobe input.mp4
ffmpeg -i input.mp4 -vn output.m4a
ffmpeg -ss 00:00:10 -i input.mp4 -t 5 clip.mp4
```

These examples create output files. Codec/container compatibility depends on the input and chosen output.

### glow

[Project / documentation](https://github.com/charmbracelet/glow) · Homebrew: `glow`.

Render Markdown in the terminal.

```sh
glow README.md
glow -p docs/index.md
printf "# Hello\n" | glow -
```

### ImageMagick

[Project / documentation](https://imagemagick.org) · Homebrew: `imagemagick`.

Batch-convert, resize, and inspect images. Executable: magick.

```sh
magick identify photo.jpg
magick photo.jpg -resize '1600x1600>' resized.jpg
magick input.png output.webp
```

These examples preserve the named input and create separate output files.

### Chafa

[Project / documentation](https://hpjansson.org/chafa/) · Homebrew: `chafa`.

Render images using terminal-supported graphics or character output.

```sh
chafa image.png
chafa --format symbols image.png
chafa --help
```

---

[← Previous: Networking and cloud files](networking.md) · [Docs index](../index.md) · [Next: System overview →](system.md)
