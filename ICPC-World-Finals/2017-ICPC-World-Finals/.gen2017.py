# -*- coding: utf-8 -*-
"""Generate 2017 ICPC World Finals problem HTML pages. Temporary build script."""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__)) + '/problems'

STYLE = """  :root {
    --text: #1a1a1a;
    --muted: #555;
    --accent: #1a56b0;
    --rule: #d0d0d0;
    --bg: #fff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0 auto;
    max-width: 46rem;
    padding: 2.5rem 1.25rem 3rem;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.0625rem;
    line-height: 1.6;
    color: var(--text);
    background: var(--bg);
  }
  header {
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.75rem;
    margin-bottom: 1.75rem;
  }
  header .kicker {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 0.35rem;
  }
  header h1 {
    font-size: 1.9rem;
    line-height: 1.2;
    margin: 0 0 0.4rem;
  }
  header .meta {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 0.9rem;
    color: var(--muted);
    margin: 0;
  }
  h2 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 1.25rem;
    margin: 2rem 0 0.75rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--rule);
  }
  h3 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 1rem;
    margin: 1.5rem 0 0.5rem;
  }
  p { margin: 0 0 1rem; }
  figure {
    margin: 1.5rem 0;
    text-align: center;
  }
  figure.hero {
    float: right;
    width: 260px;
    margin: 0 0 1rem 1.5rem;
  }
  figure img {
    max-width: 100%;
    height: auto;
    border: 1px solid var(--rule);
    border-radius: 4px;
  }
  figcaption {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.5rem;
  }
  pre {
    background: #f6f7f9;
    border: 1px solid var(--rule);
    border-left: 4px solid var(--accent);
    border-radius: 4px;
    padding: 0.75rem 1rem;
    overflow-x: auto;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.9rem;
    line-height: 1.45;
    margin: 0 0 1rem;
    white-space: pre;
  }
  footer {
    margin-top: 2.5rem;
    padding-top: 0.75rem;
    border-top: 2px solid var(--accent);
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    text-align: center;
  }
  @media (max-width: 600px) {
    figure.hero { float: none; width: 100%; margin: 1.5rem 0; }
  }

  .backlink { margin: 0 0 1.25rem; font-family: "Helvetica Neue", Arial, sans-serif; font-size: 0.85rem; }
  .backlink a { color: var(--accent); text-decoration: none; }
  .backlink a:hover { text-decoration: underline; }"""

def page(letter, title, timelimit, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Problem {letter}: {title} — ACM-ICPC World Finals 2017</title>
<style>
{STYLE}
</style>
</head>
<body>
<p class="backlink"><a href="index.html">← All problems</a></p>


<header>
  <p class="kicker">ACM-ICPC World Finals 2017 · Problem {letter}</p>
  <h1>{title}</h1>
  <p class="meta">Time limit: {timelimit}</p>
</header>

{body}
<footer>
  ACM-ICPC World Finals 2017 Problem {letter}: {title}
</footer>

</body>
</html>
"""

def si(n, text):
    return f"<h3>Sample Input {n}</h3>\n<pre>{text}</pre>"

def so(n, text):
    return f"<h3>Sample Output {n}</h3>\n<pre>{text}</pre>"

def fig(src, caption=None, cls=None):
    c = f"\n  <figcaption>{caption}</figcaption>" if caption else ""
    tag = f'<figure class="{cls}">' if cls else '<figure>'
    return f"{tag}\n  <img src=\"images/{src}\" alt=\"\">{c}\n</figure>"

B = page('B', 'Get a Clue!', '4 seconds', """
<p>Developed in the 1940s in the United Kingdom, the game of Cluedo is one of
the most popular board games in the world. The object of the game is to
determine who murdered Mr. Body, which weapon was used to murder him, and where
the murder took place. The game uses a set of cards representing six persons
(labeled A, B, &hellip;, F), six weapons (labeled G, H, &hellip;, L) and nine
rooms (labeled M, N, &hellip;, U). At the start of the game, one person card,
one weapon card, and one room card are selected at random and removed from the
deck so no one can see them – they represent the murderer, the murder weapon,
and the murder location. The remaining 18 cards are shuffled and dealt to the
players, starting with player 1, then to her right player 2, and so on. Some
players may end up with one more card than others. For the purposes of this
problem there are four players, so the person to the right of player 4 is
player 1.</p>

<p>The rest of the game is spent searching for clues. Players take turns,
starting with player 1 and moving to the right. A turn consists of making a
suggestion (consisting of a murder suspect, a weapon, and a room) and asking
other players if they have any evidence that refutes the suggestion. For
example, you might say to another player &ldquo;I believe the murderer was
person A, using weapon L, in room T.&rdquo; If the other player is holding
exactly one of these cards, that player must show you (and only you) that card.
If they have more than one such card, they can show you any one of them.</p>

<p>When making a suggestion, you must first ask the person to your right for
any evidence. If they have none, you continue with the person on their right,
and so on, until someone has evidence, or no one has any of the cards in your
suggestion.</p>

<p>Many times you can gain information even if you are not the person making
the suggestion. Suppose, in the above example, you are the third player and
have cards A and T. If someone else shows evidence to the suggester, you know
that it must be weapon card L. Keeping track of suggestions and who gave
evidence at each turn is an important strategy when playing the game.</p>

<p>To win the game, you must make an accusation, where you state your final
guess of the murderer, weapon, and room. After stating your accusation, you
check the three cards that were set aside at the start of the game – if they
match your accusation, you win! Needless to say, you want to be absolutely sure
of your accusation before you make it.</p>

<p>Here is your problem. You are player 1. Given a set of cards dealt to you
and a history of suggestions and evidence, you need to decide how close you are
to being able to make an accusation.</p>

<h2>Input</h2>

<p>The input starts with an integer <i>n</i> (1 &le; <i>n</i> &le; 50), the
number of suggestions made during the game. Following this is a line containing
the five cards you are dealt, all uppercase letters in the range &lsquo;A&rsquo;
&hellip; &lsquo;U&rsquo;. The remaining <i>n</i> lines contain one suggestion
per line. Each of these lines starts with three characters representing the
suggestion (in the order person, weapon, room), followed by the responses of up
to three players, beginning with the player to the right of the player making
the suggestion. If a player presents no evidence, a &lsquo;-&rsquo; (dash) is
listed; otherwise an &ldquo;evidence character&rdquo; is listed. If the specific
evidence card is seen by you (either because you provided it or you were the
person receiving the evidence) then the evidence character identifies that card;
otherwise the evidence character is &lsquo;*&rsquo;. Note that only the last
response can be an evidence character. All characters are separated by single
spaces. Only valid suggestion/response sequences appear in the input.</p>

<h2>Output</h2>

<p>Display a three character string identifying the murderer, the murder weapon,
and the room. If the murderer can be identified, use the appropriate letter for
that person; otherwise use &lsquo;?&rsquo;. Do the same for the murder weapon
and the room.</p>

""" + si(1, "1\nB I P C F\nA G M - - -") + "\n\n" + so(1, "AGM") + "\n\n"
     + si(2, "2\nA B C D H\nF G M M\nF H M - *") + "\n\n" + so(2, "E??") + "\n\n"
     + si(3, "3\nA C M S D\nB G S - G\nA H S - - S\nC J S *") + "\n\n" + so(3, "???"))

C = page('C', 'Mission Improbable', '1 second', """
<p>It is a sunny day in spring and you are about to meet Patrick, a close
friend and former partner in crime. Patrick lost most of his money betting on
programming contests, so he needs to pull off another job. For this he needs
your help, even though you have retired from a life of crime. You are reluctant
at first, as you have no desire to return to your old criminal ways, but you
figure there is no harm in listening to his plan.</p>

<p>There is a shipment of expensive consumer widgets in a nearby warehouse and
Patrick intends to steal as much of it as he can. This entails finding a way
into the building, incapacitating security guards, passing through various
arrays of laser beams – you know, the usual heist techniques. However, the
heart of the warehouse has been equipped with a security system that Patrick
cannot disable. This is where he needs your help.</p>

<p>The shipment is stored in large cubical crates, all of which have the same
dimensions. The crates are stacked in neat piles, forming a three-dimensional
grid. The security system takes pictures of the piles once per hour using three
cameras: a front camera, a side camera and a top camera. The image from the
front camera shows the height of the tallest pile in each column, the image
from the side camera shows the height of the tallest pile in each row, and the
image from the top camera shows whether or not each pile is empty. If the
security system detects a change in any of the images, it sounds an alarm.</p>

<p>Once Patrick is inside, he will determine the heights of the piles and send
them to you. Figure C.1 shows a possible layout of the grid and the view from
each of the cameras.</p>

""" + fig('C-1.png', 'Figure C.1: Grid of heights and the corresponding camera views.') + """

<p>Patrick wants to steal as many crates as possible. Since he cannot disable
the security system, he plans to fool it by arranging the remaining crates into
piles so that the next set of camera images are the same. In the above example,
it is possible to steal nine crates. Figure C.2 shows one possible post-heist
configuration that appears identical to the security system.</p>

""" + fig('C-2.png', 'Figure C.2: Possible grid of heights after the heist') + """

<p>Patrick asks you to help him determine the maximum number of crates that can
be stolen while leaving a configuration of crates that will fool the security
system. Will you help him pull off this final job?</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>r</i> (1 &le; <i>r</i>
&le; 100) and <i>c</i> (1 &le; <i>c</i> &le; 100), the number of rows and
columns in the grid, respectively. Each of the following <i>r</i> lines
contains <i>c</i> integers, the heights (in crates) of the piles in the
corresponding row. All heights are between 0 and 10<sup>9</sup> inclusive.</p>

<h2>Output</h2>

<p>Display the maximum number of crates that can be stolen without being
detected.</p>

""" + si(1, "5 5\n1 4 0 5 2\n2 1 2 0 1\n0 2 3 4 4\n0 3 0 3 1\n1 2 2 1 1") + "\n\n"
     + so(1, "9") + "\n\n" + si(2, "2 3\n50 20 3\n20 10 3") + "\n\n" + so(2, "30"))

D = page('D', 'Money for Nothing', '5 seconds', """
<p>In this problem you will be solving one of the most profound challenges of
humans across the world since the beginning of time – how to make lots of
money.</p>

<p>You are a middleman in the widget market. Your job is to buy widgets from
widget producer companies and sell them to widget consumer companies. Each
widget consumer company has an open request for one widget per day, until some
end date, and a price at which it is willing to buy the widgets. On the other
hand, each widget producer company has a start date at which it can start
delivering widgets and a price at which it will deliver each widget.</p>

<p>Due to fair competition laws, you can sign a contract with only one producer
company and only one consumer company. You will buy widgets from the producer
company, one per day, starting on the day it can start delivering, and ending
on the date specified by the consumer company. On each of those days you earn
the difference between the producer&rsquo;s selling price and the
consumer&rsquo;s buying price.</p>

<p>Your goal is to choose the consumer company and the producer company that
will maximize your profits.</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>m</i> and <i>n</i> (1
&le; <i>m</i>, <i>n</i> &le; 500&thinsp;000) denoting the number of producer
and consumer companies in the market, respectively. It is followed by <i>m</i>
lines, the <i>i</i>th of which contains two integers <i>p</i><sub><i>i</i></sub>
and <i>d</i><sub><i>i</i></sub> (1 &le; <i>p</i><sub><i>i</i></sub>,
<i>d</i><sub><i>i</i></sub> &le; 10<sup>9</sup>), the price (in dollars) at
which the <i>i</i>th producer sells one widget and the day on which the first
widget will be available from this company. Then follow <i>n</i> lines, the
<i>j</i>th of which contains two integers <i>q</i><sub><i>j</i></sub> and
<i>e</i><sub><i>j</i></sub> (1 &le; <i>q</i><sub><i>j</i></sub>,
<i>e</i><sub><i>j</i></sub> &le; 10<sup>9</sup>), the price (in dollars) at
which the <i>j</i>th consumer is willing to buy widgets and the day immediately
after the day on which the last widget has to be delivered to this company.</p>

<h2>Output</h2>

<p>Display the maximum total number of dollars you can earn. If there is no way
to sign contracts that gives you any profit, display 0.</p>

""" + si(1, "2 2\n1 3\n2 1\n3 5\n7 2") + "\n\n" + so(1, "5") + "\n\n"
     + si(2, "1 2\n10 10\n9 11\n11 9") + "\n\n" + so(2, "0"))

E = page('E', 'Need for Speed', '1 second', """
""" + fig('E-1.png', None, 'hero') + """

<p>Sheila is a student and she drives a typical student car: it is old, slow,
rusty, and falling apart. Recently, the needle on the speedometer fell off. She
glued it back on, but she might have placed it at the wrong angle. Thus, when
the speedometer reads <i>s</i>, her true speed is <i>s</i> + <i>c</i>, where
<i>c</i> is an unknown constant (possibly negative).</p>

<p>Sheila made a careful record of a recent journey and wants to use this to
compute <i>c</i>. The journey consisted of <i>n</i> segments. In the
<i>i</i>th segment she traveled a distance of <i>d</i><sub><i>i</i></sub> and
the speedometer read <i>s</i><sub><i>i</i></sub> for the entire segment. This
whole journey took time <i>t</i>. Help Sheila by computing <i>c</i>.</p>

<p>Note that while Sheila&rsquo;s speedometer might have negative readings, her
true speed was greater than zero for each segment of the journey.</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>n</i> (1 &le; <i>n</i>
&le; 1&thinsp;000), the number of sections in Sheila&rsquo;s journey, and
<i>t</i> (1 &le; <i>t</i> &le; 10<sup>6</sup>), the total time. This is
followed by <i>n</i> lines, each describing one segment of Sheila&rsquo;s
journey. The <i>i</i>th of these lines contains two integers
<i>d</i><sub><i>i</i></sub> (1 &le; <i>d</i><sub><i>i</i></sub> &le;
1&thinsp;000) and <i>s</i><sub><i>i</i></sub> (|<i>s</i><sub><i>i</i></sub>|
&le; 1&thinsp;000), the distance and speedometer reading for the <i>i</i>th
segment of the journey. Time is specified in hours, distance in miles, and
speed in miles per hour.</p>

<h2>Output</h2>

<p>Display the constant <i>c</i> in miles per hour. Your answer should have an
absolute or relative error of less than 10<sup>&minus;6</sup>.</p>

""" + si(1, "3 5\n4 -1\n4 0\n10 3") + "\n\n" + so(1, "3.000000000") + "\n\n"
     + si(2, "4 10\n5 3\n2 2\n3 6\n3 1") + "\n\n" + so(2, "-0.508653377"))

F = page('F', 'Posterize', '2 seconds', """
""" + fig('F-1.png') + """

<p>Pixels in a digital picture can be represented with three integers in the
range 0 to 255 that indicate the intensity of the red, green, and blue colors.
To compress an image or to create an artistic effect, many photo-editing tools
include a &ldquo;posterize&rdquo; operation which works as follows. Each color
channel is examined separately; this problem focuses only on the red channel.
Rather than allow all integers from 0 to 255 for the red channel, a
posterized image allows at most <i>k</i> integers from this range. Each
pixel&rsquo;s original red intensity is replaced with the nearest of the
allowed integers. The photo-editing tool selects a set of <i>k</i> integers
that minimizes the sum of the squared errors introduced across all pixels in
the original image. If there are <i>n</i> pixels that have original red values
<i>r</i><sub>1</sub>, &hellip;, <i>r</i><sub><i>n</i></sub>, and <i>k</i>
allowed integers <i>v</i><sub>1</sub>, &hellip;, <i>v</i><sub><i>k</i></sub>,
the sum of squared errors is defined as &sum;<sub><i>i</i>=1</sub><sup><i>n</i></sup>
min<sub>1&le;<i>j</i>&le;<i>k</i></sub> (<i>r</i><sub><i>i</i></sub> &minus;
<i>v</i><sub><i>j</i></sub>)<sup>2</sup>.</p>

<p>Your task is to compute the minimum achievable sum of squared errors, given
parameter <i>k</i> and a description of the red intensities of an
image&rsquo;s pixels.</p>

<h2>Input</h2>

<p>The first line of the input contains two integers <i>d</i> (1 &le;
<i>d</i> &le; 256), the number of distinct red values that occur in the
original image, and <i>k</i> (1 &le; <i>k</i> &le; <i>d</i>), the number of
distinct red values allowed in the posterized image. The remaining <i>d</i>
lines indicate the number of pixels of the image having various red values.
Each such line contains two integers <i>r</i> (0 &le; <i>r</i> &le; 255) and
<i>p</i> (1 &le; <i>p</i> &le; 2<sup>26</sup>), where <i>r</i> is a red
intensity value and <i>p</i> is the number of pixels having red intensity
<i>r</i>. Those <i>d</i> lines are given in increasing order of red value.</p>

<h2>Output</h2>

<p>Display the sum of the squared errors for an optimally chosen set of
<i>k</i> allowed integer values.</p>

""" + si(1, "2 1\n50 20000\n150 10000") + "\n\n" + so(1, "66670000") + "\n\n"
     + si(2, "2 2\n50 20000\n150 10000") + "\n\n" + so(2, "0") + "\n\n"
     + si(3, "4 2\n0 30000\n25 30000\n50 30000\n255 30000") + "\n\n" + so(3, "37500000"))

G = page('G', 'Replicate Replicate Rfplicbte', '3 seconds', """
<p>The owner of the Automatic Cellular Manufacturing corporation has just
patented a new process for the mass production of identical parts. Her approach
uses a two-dimensional lattice of two-state cells, each of which is either
&ldquo;empty&rdquo; or &ldquo;filled.&rdquo; The exact details are, of course,
proprietary.</p>

<p>Initially, a set of cells in the lattice is filled with a copy of the part
that is to be reproduced. In a sequence of discrete steps, each cell in the
lattice simultaneously updates its state by examining its own state and those
of its eight surrounding neighbors. If an odd number of these nine cells are
filled, the cell&rsquo;s state in the next time step will be filled, otherwise
it will be empty. Figure G.1 shows several steps in the replication process for
a simple pattern consisting of three filled cells.</p>

""" + fig('G-1.png', 'Figure G.1: The replication process.') + """

<p>However, a bug has crept into the process. After each update step, one cell
in the lattice might spontaneously flip its state. For instance, Figure G.2
shows what might happen if a cell flipped its state after the first time step
and another flipped its state after the third time step.</p>

""" + fig('G-2.png', 'Figure G.2: Errors in the replication process. This figure corresponds to Sample Input 1.') + """

<p>Unfortunately, the original patterns were lost, and only the (possibly
corrupted) results of the replication remain. Can you write a program to
determine a smallest possible nonempty initial pattern that could have resulted
in a given final pattern?</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>w</i> (1 &le; <i>w</i>
&le; 300) and <i>h</i> (1 &le; <i>h</i> &le; 300), where <i>w</i> and
<i>h</i> are the width and height of the bounding box of the final pattern.
Following that are <i>h</i> lines, each containing <i>w</i> characters, giving
the final pattern. Each character is either &lsquo;.&rsquo; (representing an
empty cell) or &lsquo;#&rsquo; (representing a filled cell). There is at least
one filled cell in the first row, in the last row, in the first column, and in
the last column.</p>

<h2>Output</h2>

<p>Display a minimum-size nonempty pattern that could have resulted in the
given pattern, assuming that at each stage of the replication process at most
one cell spontaneously changed state. The size of a pattern is the area of its
bounding box. If there is more than one possible minimum-size nonempty starting
pattern, any one will be accepted. Use the character &lsquo;.&rsquo; for empty
cells and &lsquo;#&rsquo; for filled cells. Use the minimum number of rows and
columns needed to display the pattern.</p>

""" + si(1, "10 10\n.#...#...#\n##..##..##\n##.#.##...\n##.#.##...\n.#...#####\n...##..#.#\n......###.\n##.#.##...\n#..#..#..#\n##..##..##") + "\n\n"
     + so(1, ".#\n##") + "\n\n"
     + si(2, "8 8\n##..#.##\n#.####.#\n.#.#.#..\n.##.#.##\n.#.#.#..\n.##.#.##\n#..#.###\n##.#.##.") + "\n\n"
     + so(2, "####\n#..#\n#.##\n###.") + "\n\n"
     + si(3, "5 4\n#....\n..###\n..###\n..###") + "\n\n" + so(3, "#"))

H = page('H', 'Scenery', '6 seconds', """
""" + fig('H-1.png', 'Images by John Fowler, Carol Highsmith, and Richard Woodland') + """

<p>You have decided to spend a day of your trip to Rapid City taking
photographs of the South Dakota Badlands, which are renowned for their
spectacular and unusual land formations. You are an amateur photographer, yet
very particular about lighting conditions.</p>

<p>After some careful research, you have located a beautiful location in the
Badlands, surrounded by picturesque landscapes. You have determined a variety
of features that you wish to photograph from this location. For each feature you
have identified the earliest and latest time of day at which the position of
the sun is ideal. However, it will take quite a bit of time to take each
photograph, given the need to reposition the tripod and camera and your general
perfectionism. So you are wondering if it will be possible to successfully take
photographs of all these features in one day.</p>

<h2>Input</h2>

<p>The first line of the input contains two integers <i>n</i> (1 &le;
<i>n</i> &le; 10<sup>4</sup>) and <i>t</i> (1 &le; <i>t</i> &le; 10<sup>5</sup>),
where <i>n</i> is the number of desired photographs and <i>t</i> is the time you
spend to take each photograph. Following that are <i>n</i> additional lines,
each describing the available time period for one of the photographs. Each such
line contains two nonnegative integers <i>a</i> and <i>b</i>, where <i>a</i> is
the earliest time that you may begin working on that photograph, and <i>b</i> is
the time by which the photograph must be completed, with <i>a</i> + <i>t</i>
&le; <i>b</i> &le; 10<sup>9</sup>.</p>

<h2>Output</h2>

<p>Display <i>yes</i> if it is possible to take all <i>n</i> photographs, and
<i>no</i> otherwise.</p>

""" + si(1, "2 10\n0 15\n5 20") + "\n\n" + so(1, "yes") + "\n\n"
     + si(2, "2 10\n1 15\n0 20") + "\n\n" + so(2, "no") + "\n\n"
     + si(3, "2 10\n5 30\n10 20") + "\n\n" + so(3, "yes"))

I = page('I', 'Secret Chamber at Mount Rushmore', '1 second', """
""" + fig('I-1.png', None, 'hero') + """

<p>By now you have probably heard that there is a spectacular stone sculpture
featuring four famous U.S. presidents at Mount Rushmore. However, very few
people know that this monument contains a secret chamber. This sounds like
something out of a plot of a Hollywood movie, but the chamber really exists. It
can be found behind the head of Abraham Lincoln and was designed to serve as a
Hall of Records to store important historical U.S. documents and artifacts.
Historians claim that the construction of the hall was halted in 1939 and the
uncompleted chamber was left untouched until the late 1990s, but this is not the
whole truth.</p>

<p>In 1982, the famous archaeologist S. Dakota Jones secretly visited the
monument and found that the chamber actually was completed, but it was kept
confidential. This seemed suspicious and after some poking around, she found a
hidden vault and some documents inside. Unfortunately, these documents did not
make any sense and were all gibberish. She suspected that they had been written
in a code, but she could not decipher them despite all her efforts.</p>

<p>Earlier this week when she was in the area to follow the ACM-ICPC World
Finals, Dr. Jones finally discovered the key to deciphering the documents, in
Connolly Hall of SDSM&amp;T. She found a document that contains a list of
translations of letters. Some letters may have more than one translation, and
others may have no translation. By repeatedly applying some of these
translations to individual letters in the gibberish documents, she might be able
to decipher them to yield historical U.S. documents such as the Declaration of
Independence and the Constitution. She needs your help.</p>

<p>You are given the possible translations of letters and a list of pairs of
original and deciphered words. Your task is to verify whether the words in each
pair match. Two words match if they have the same length and if each letter of
the first word can be turned into the corresponding letter of the second word
by using the available translations zero or more times.</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>m</i> (1 &le; <i>m</i>
&le; 500) and <i>n</i> (1 &le; <i>n</i> &le; 50), where <i>m</i> is the number
of translations of letters and <i>n</i> is the number of word pairs. Each of the
next <i>m</i> lines contains two distinct space-separated letters <i>a</i> and
<i>b</i>, indicating that the letter <i>a</i> can be translated to the letter
<i>b</i>. Each ordered pair of letters (<i>a</i>, <i>b</i>) appears at most
once. Following this are <i>n</i> lines, each containing a word pair to check.
Translations and words use only lowercase letters &lsquo;a&rsquo;&ndash;&lsquo;z&rsquo;,
and each word contains at least 1 and at most 50 letters.</p>

<h2>Output</h2>

<p>For each pair of words, display <i>yes</i> if the two words match, and
<i>no</i> otherwise.</p>

""" + si(1, "9 5\nc t\ni r\nk p\no c\nr o\nt e\nt f\nu h\nw p\nwe we\ncan the\nwork people\nit of\nout the") + "\n\n"
     + so(1, "yes\nno\nno\nyes\nyes") + "\n\n"
     + si(2, "3 3\na c\nb a\na b\naaa abc\nabc aaa\nacm bcm") + "\n\n"
     + so(2, "yes\nno\nyes"))

J = page('J', 'Son of Pipe Stream', '5 seconds', """
<p>Two years ago, you helped install the nation&rsquo;s very first Flubber pipe
network in your hometown, to great success. Polls show that everyone loves
having their own Flubber dispenser in their kitchen, and now a few
enterprising citizens have discovered a use for it. Apparently Flubber, when
mixed with water, can help extinguish fires! This is a very timely discovery,
as out-of-control fires have lately been surprisingly common.</p>

<p>Your hometown&rsquo;s city council would like to make use of this property of
Flubber by creating the Flubber/water mixture at a centrally located station.
This station, which is called the Flubber Department (FD) will also have
specialized employees trained to travel to the locations of fires and make use
of their processed Flubber to control the blazes.</p>

<p>The pipes are already in place all around the city. You are given a layout of
the pipes, and must determine how to route Flubber from the Flubber factory and
water from a local source through the pipes to the FD. Note that both Flubber
and water will be flowing through the same network of pipes, perhaps even the
same pipe. All pipes are bidirectional, but Flubber and water cannot move in
opposite directions through the same pipe. Furthermore, if both liquids are sent
in the same direction through the same pipe, they will inevitably mix. Therefore
the nodes in the network have been equipped with special membranes and filters
that enable you to separate and reorganize all incoming mixtures as you see fit.
The network is a closed system, so the total rate of each fluid going into a
node must equal the total rate of that fluid going out, except at the source of
that fluid and the destination (the FD).</p>

<p>Each pipe has a certain capacity. Flubber, being somewhat sluggish, has a
viscosity value <i>v</i>, so a pipe that can transport <i>v</i> liters/second of
water can transport only 1 liter/second of Flubber. The pipe&rsquo;s capacity
scales linearly for mixtures of the two. To be precise, if <i>c</i> denotes the
water capacity of the pipe and <i>f</i> and <i>w</i> are the rates of Flubber
and water moving through the pipe (all measured in liters/second), then the
capacity constraint is given by the inequality <i>v</i> &middot; <i>f</i> +
<i>w</i> &le; <i>c</i>.</p>

<p>Your main concern is balancing the mixture that reaches the FD. You would
like as much total liquid as possible, but you also need a sufficient amount of
water – because undiluted Flubber is highly flammable – and a sufficient amount
of Flubber – because it would not be much of a &ldquo;Flubber Department&rdquo;
without Flubber! You have come up with a formula to measure the &ldquo;value&rdquo;
of the final mixture: <i>F</i><sup><i>a</i></sup> &middot;
<i>W</i><sup>1&minus;<i>a</i></sup>, where <i>F</i> is the rate of incoming
Flubber in liters/second, <i>W</i> is the rate of incoming water in
liters/second, and <i>a</i> is a given constant between 0 and 1.</p>

<p>Determine the maximum value of <i>F</i><sup><i>a</i></sup> &middot;
<i>W</i><sup>1&minus;<i>a</i></sup> that can be achieved and how to route the
Flubber and water to achieve it.</p>

<h2>Input</h2>

<p>The input starts with a line containing the number of locations <i>n</i>
(3 &le; <i>n</i> &le; 200), the number of pipes <i>p</i> (<i>n</i> &minus; 1
&le; <i>p</i> &le; <i>n</i>(<i>n</i> &minus; 1)/2), and the real values
<i>v</i> (1 &le; <i>v</i> &le; 10) and <i>a</i> (0.01 &le; <i>a</i>
&le; 0.99). Locations are numbered from 1 to <i>n</i>; 1 is the Flubber
factory, 2 is the water source, and 3 is the FD. The real values have at most
10 digits after the decimal point.</p>

<p>The following <i>p</i> lines each describe one pipe. Each line contains two
integers <i>j</i> and <i>k</i> (1 &le; <i>j</i> &lt; <i>k</i> &le; <i>n</i>),
giving the locations connected by the pipe, and an integer <i>c</i> (1
&le; <i>c</i> &le; 10), giving the water capacity of the pipe in liters/second.
No two pipes connect the same pair of locations. Furthermore, it is guaranteed
that the network is connected.</p>

<h2>Output</h2>

<p>First, for each pipe (in the order given in the input), display two values:
the rate of Flubber moving through it, and the rate of water moving through it
(negative if the liquid is moving from <i>k</i> to <i>j</i>), such that
<i>F</i><sup><i>a</i></sup> &middot; <i>W</i><sup>1&minus;<i>a</i></sup> is
maximized. Then display that maximum value accurate to within an absolute error
of 10<sup>&minus;4</sup>. If there are multiple solutions, any one will be
accepted. All constraints (not sending Flubber and water in opposite directions
along the same pipe, flow conservation, pipe capacities, and consistency between
the constructed solution and its claimed value) must be satisfied within an
absolute error of 10<sup>&minus;4</sup>.</p>

""" + si(1, "6 6 3.0 0.66\n2 4 8\n4 6 1\n3 6 1\n4 5 5\n1 5 7\n3 5 3") + "\n\n"
     + so(1, "0.000000000 1.360000000\n0.000000000 1.000000000\n0.000000000 -1.000000000\n0.000000000 0.360000000\n0.880000000 0.000000000\n-0.880000000 -0.360000000\n1.02037965897") + "\n\n"
     + si(2, "5 5 1.0 0.5\n1 2 10\n2 3 10\n3 4 10\n4 5 10\n3 5 10") + "\n\n"
     + so(2, "5 0\n5 5\n4.2 3.14159\n4.2 3.14159\n-4.2 -3.14159\n5"))

K = page('K', 'Tarot Sham Boast', '2 seconds', """
<p>Curse your rival! Every year at the annual Rock Paper Scissors tournament,
you have made it to the final match. (Your Rock technique is unmatched, and your
Paper cuts to the bone! Your Scissors need a little work, though.) But every
year, he defeats you, even though his moves appear entirely random! And he
claims to the press that he simply cannot be beaten. What is his secret?</p>

<p>Fortunately, you think you have figured it out. This year, just before the
tournament, you caught him visiting various shamans around town. Aha! He is
using the supernatural against you! You figured two can play at this game. So
you went and visited a set of fortune-tellers, who have each used a Tarot deck
to predict a sequence that your rival will end up using, sometime during the
match.</p>

<p>However, your initial excitement has passed, and now you are feeling a little
silly. This cannot possibly work, right? In the end it feels like you have paid
good money for a fraudulent, random set of predictions. Oh well; you might as
well keep an eye out for some of them during the match. But which predictions
will you use?</p>

<p>In the final match, you and your rival will play <i>n</i> rounds of Rock
Paper Scissors. In each round, your rival and you will both choose one of the
three options (Rock, Paper, or Scissors). Based on your selections, a winner of
the round will be determined (exactly how is irrelevant to this problem).</p>

<p>Given the length of the final match and the various predictions, sort them in
order of how likely they are to appear sometime during the match as a contiguous
sequence of options chosen by your rival, assuming he is choosing his symbol in
each round independently and uniformly at random.</p>

<h2>Input</h2>

<p>The first line of input contains two integers <i>n</i> (1 &le; <i>n</i>
&le; 10<sup>6</sup>), the number of rounds in the final match, and <i>s</i>
(1 &le; <i>s</i> &le; 10), the number of sequences. The remaining <i>s</i> lines
each describe a prediction, consisting of a string of characters &lsquo;R&rsquo;,
&lsquo;P&rsquo;, and &lsquo;S&rsquo;. All predictions have the same length, which
is between 1 and <i>n</i> characters long, inclusive, and no longer than
10<sup>5</sup>.</p>

<h2>Output</h2>

<p>Display all of the predictions, sorted by decreasing likelihood of appearance
sometime during the final match. In the case of tied predictions, display them
in the same order as in the input.</p>

""" + si(1, "3 4\nPP\nRR\nPS\nSS") + "\n\n" + so(1, "PS\nPP\nRR\nSS") + "\n\n"
     + si(2, "20 3\nPRSPS\nSSSSS\nPPSPP") + "\n\n" + so(2, "PRSPS\nPPSPP\nSSSSS"))

L = page('L', 'Visual Python++', '5 seconds', """
<p>In the recently proposed Visual Python++ programming language, a block of
statements is represented as a rectangle of characters with top-left corner in
row <i>r</i><sub>1</sub> and column <i>c</i><sub>1</sub>, and bottom-right
corner in row <i>r</i><sub>2</sub> and column <i>c</i><sub>2</sub>. All
characters at locations (<i>r</i>, <i>c</i>) with <i>r</i><sub>1</sub>
&le; <i>r</i> &le; <i>r</i><sub>2</sub> and <i>c</i><sub>1</sub> &le; <i>c</i>
&le; <i>c</i><sub>2</sub> are then considered to belong to that block. Among
these locations, the ones with <i>r</i> = <i>r</i><sub>1</sub> or
<i>r</i> = <i>r</i><sub>2</sub> or <i>c</i> = <i>c</i><sub>1</sub> or
<i>c</i> = <i>c</i><sub>2</sub> are called a border.</p>

<p>Statement blocks can be nested (rectangles contained in other rectangles) to
an arbitrary level. In a syntactically correct program, every two statement
blocks are either nested (one contained in the other) or disjoint (not
overlapping). In both cases, their borders may not overlap.</p>

<p>Programmers are not expected to draw the many rectangles contained in a
typical program – this takes too long, and Visual Python++ would not have a
chance to become the next ICPC programming language. So a programmer only has to
put one character &lsquo;p&rsquo; in the top-left corner of the rectangle and one
character &lsquo;y&rsquo; in the bottom-right corner. The parser will
automatically match up the appropriate corners to obtain the nesting structure
of the program.</p>

<p>Your team has just been awarded a five-hour contract to develop this part of
the parser.</p>

<h2>Input</h2>

<p>The first line of the input contains an integer <i>n</i> (1 &le; <i>n</i>
&le; 10<sup>5</sup>), the number of corner pairs. Each of the next <i>n</i>
lines contains two integers <i>r</i> and <i>c</i> (1 &le; <i>r</i>,
<i>c</i> &le; 10<sup>9</sup>), specifying that there is a top-left corner in row
<i>r</i> and column <i>c</i> of the program you are parsing. Following that are
<i>n</i> lines specifying the bottom-right corners in the same way. All corner
locations are distinct.</p>

<h2>Output</h2>

<p>Display <i>n</i> lines, each containing one integer. A number <i>j</i> in
line <i>i</i> means that the <i>i</i>th top-left corner and the <i>j</i>th
bottom-right corner form one rectangle. Top-left and bottom-right corners are
each numbered from 1 to <i>n</i> in the order they appear in the input. The
output must be a permutation of the numbers from 1 to <i>n</i> such that the
matching results in properly nested rectangles. If there is more than one valid
matching, any one will be accepted. If no such matching exists, display
<i>syntax error</i>.</p>

""" + si(1, "2\n4 7\n9 8\n14 17\n19 18") + "\n\n" + so(1, "2\n1") + "\n\n"
     + si(2, "2\n4 7\n14 17\n9 8\n19 18") + "\n\n" + so(2, "1\n2") + "\n\n"
     + si(3, "2\n4 8\n9 7\n14 18\n19 17") + "\n\n" + so(3, "syntax error") + "\n\n"
     + si(4, "3\n1 1\n4 8\n8 4\n10 6\n6 10\n10 10") + "\n\n" + so(4, "syntax error"))

for letter, html in [('B', B), ('C', C), ('D', D), ('E', E), ('F', F), ('G', G),
                     ('H', H), ('I', I), ('J', J), ('K', K), ('L', L)]:
    path = os.path.join(OUT, letter + '.html')
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', path, len(html))
print('done')
