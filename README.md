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

1. Copy this repo
2. Establish and copy the right GitHub token, prefrably with limited premissions, and only for the new repo. 
(GitHub Settings -> Developer setting (bottom of the page) -> Personal access tokens -> Fine grained tokens (Not a 100% sure how to tune, I allowed for everythin))
3. Build and launch with docker (see below) - enter the necessary parameters during launch. 
4. Add more patterns if you want - I recommend pasting the code into an AI chatbot, and asking it for more patterns


Remember to docker build with arguments

```console
docker build --build-arg GIT_USER="username" --build-arg GIT_EMAIL="email" -t make-commits .  
```
```console
docker run -it make-commits 
```

### Watch out
I get it - the way the tokens are passed is not pretty. 

But I did not want it saved anywhere, so passing like this seemed like the best option.

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