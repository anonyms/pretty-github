# pretty-github
Making my GitHub contributions view pretty, ie adding icons and such.


Pretty pointless stuff really, just wanted to try doing it through Genai Chat bots, all code written through them, with some very minor tweaks I just did without going through them.

### Learnings - coding with GenAi
I whish I had taken more notes building this, but overall
- Impressive interacting with the Gen AIs to beging with, but it definetly helped that I knew some coding, and could give some indications as to what I wanted.
- I did ask it for alternatives, and it had good proposals. It did however later on mix solution alternatives, even though I stated I had picked on of the alternatives. Example: Docker file, or docker-compose. I chose going for one docker file, but later one it gave ideas around an .env file and docker-compose.
- There were moments were it just was not able to quite adapt, and where I did a fix myself, seeing what direction the fix had to be inn, or did a quick internet search.
- The true struggle was with patterns. There was a lot of back and forth, and heavily guided prompts, in order to create a good solution. I also had to manually go in and create most of the paterns. What impressed me was when I asked for the patterns to be transposed, this was resolved on the spot.


### Usage

Needs [uv](https://docs.astral.sh/uv/), make (on Windows: `winget install ezwinports.make`)
and the [GitHub CLI](https://cli.github.com/) logged in (`gh auth login`), which is used to
read your current graph.

1. Look at a pattern on your graph first; nothing is committed. The start date is the
   top-left cell of the pattern, written YYYY-MM-DD, and must be a Sunday. Without START,
   the preview uses 2022-03-06.

   ```console
   make preview PATTERN=heart START=2024-03-03
   ```

2. Make the commits. This shows the same preview, then asks before committing to `main` and
   again before pushing. It must be run on `main`, level with GitHub.

   ```console
   make commits PATTERN=heart START=2024-03-03
   ```

GitHub only counts the commits if your git email (`git config user.email`) is verified on your
account.

### Adding patterns

Each pattern is a text file in `patterns/`, named after the pattern (`patterns/heart.txt` is
`PATTERN=heart`). It has 7 lines, one per weekday from Sunday to Saturday: a digit is the
number of commits that day and a dot is none. Lines starting with `#` are comments.

```text
.1...1.
111.111
1111111
.11111.
..111..
...1...
.......
```

`make preview` shows how a new one comes out, and `make test` checks every file.

Or make one from a picture, pasted as a URL or given as a file. Quote the URL, since
PowerShell does not accept `&` unquoted:

```console
make image IMAGE="https://example.com/cat.png" NAME=cat
make preview PATTERN=cat START=2022-03-06
```

The picture is cropped, shrunk to 7 rows and its darkness turned into shades; light and
transparent parts stay blank. Add `INVERT=1` for a light drawing on a dark background.
Seven rows is tiny, so simple, high-contrast pictures (icons, emoji, pixel art) work best.
PNG, JPEG, GIF and WebP work; SVG does not.

### Development

Run `make` to list the targets, e.g. `make test` and `make lint`.

Version 1 (early 2025) ran from a Dockerfile and asked for a GitHub token to push; it is in
the git history if you want to look back.

### Honorable mentions

- [gitfiti](https://github.com/gelstudios/gitfiti) main source of inspiration - notably for this list :)
- [PixelHub](https://github.com/behind24proxies/PixelHub), where you can draw what you want, download a file, and then reproduce it in commit
- [Vincent Van Git](https://github.com/jh3y/vincent-van-git) Vincent, which offers a [very slick web ui](https://vincent-van-git.netlify.app/) to generate a gitfiti script
- [github-calendar-customerizer](https://github.com/ZachSaucier/github-calendar-customizer) from ZachSaucier, another very [nice web GUI](https://codepen.io/ZachSaucier/full/PzVRBy) for generating gitfiti templates
- [git-art](https://github.com/jamesjarvis/git-art) from jamesjarvis, a work-alike web based [editor GUI](https://jamesjarvis.github.io/git-art/) that generates the script too
- [Pikesley's](https://github.com/pikesley) Pokrovsky, which offers Github History Vandalism [as a Service!](http://pokrovsky.herokuapp.com/)
- [PSVandalism](https://github.com/DenisBalan/PSVandalism) Wrapper around Pokrovsky, which makes possible vandalising Github History from Powershell
- [github-board](https://github.com/bayandin/github-board) commits gitfiti from easy templates
- [ghdecoy](https://github.com/tickelton/ghdecoy) fills the contribution graph with random data (sneaky!)
- [Gitfiti Painter](http://codepen.io/cbas/pen/vOXeKV) visual drawing tool for artists to easily create templates
- [git-draw](https://github.com/ben174/git-draw) a Chrome extension which will allow you to freely draw on your commit map(!)
- [github-jack](https://github.com/tardypad/github-jack) a pure bash version with space invaders and shining creepypasta
- [github-graffiti](https://github.com/mavrk/github-graffiti) a GUI editor with a bash script to allow custom designs on your commit map
- [Paint GitHub](https://paintgithub.com/) is the most convenient way to paint your GitHub contribution graph!
- [contribution-pixel-messages](https://github.com/abulvenz/contribution-pixel-messages) generates a date plan from an editable GUI
- Seen something else? Submit a pull request or open an issue!