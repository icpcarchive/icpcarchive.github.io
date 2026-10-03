#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 2011 ICPC World Finals solution-sketch HTML pages."""
import re, os

BASE = "/home/thaind/qwen_test/ICPC-World-Finals"
YEAR = os.path.join(BASE, "2011-ICPC-World-Finals")
SOL = os.path.join(YEAR, "solutions")
os.makedirs(SOL, exist_ok=True)

COMP = "ACM ICPC World Finals 2011"

# ---- Extract inner CSS verbatim from the 2017 reference templates ----
def inner_css(path):
    html = open(path, encoding="utf-8").read()
    return re.search(r"<style>(.*?)</style>", html, re.S).group(1)

css_index = inner_css(os.path.join(BASE, "2017-ICPC-World-Finals/solutions/index.html"))
css_page = inner_css(os.path.join(BASE, "2017-ICPC-World-Finals/solutions/A.html"))

# ---- Per-problem pages ----
# (letter, title, [paragraphs])
PROBLEMS = [
("A", "To Add Or To Multiply", [
"First we note that the number of multiplications used in any solution must be small: there can be at most 29 of them (since if m > 1 using more multiplications inevitably gives us numbers larger than 10<sup>9</sup>, and if m = 1 multiplications are useless). So we’ll try all possible values g for the number of multiplication operations used by the solution.",
"Next, given the value of g we’ll have to figure out how to do the additions. For 0 ≤ i ≤ g, let us denote by h<sub>i</sub> the number of additions performed between the i’th and (i + 1)’th multiplication operations. So for example h<sub>0</sub> is the number of additions performed before the first multiplication and h<sub>g</sub> is the number of additions after the last one. Then, the resulting program transforms input x to α(x) = x·m<sup>g</sup> + a·∑<sub>i=0</sub><sup>g</sup> h<sub>i</sub>·m<sup>g−i</sup>. The constraint that the input range [p, q] is mapped to [r, s] is then equivalent with requiring that ∑<sub>i=0</sub><sup>g</sup> h<sub>i</sub>·m<sup>i</sup> lies in the interval [(r − p·m<sup>g</sup>)/a, (s − q·m<sup>g</sup>)/a]. Let us denote this new interval by [u, v]. If [u, v] contains no integers, it will be impossible to choose valid h<sub>i</sub>’s (for this choice of g). Otherwise, there is a solution.",
"To minimize the total number of operations, i.e., the sum of the h<sub>i</sub>’s (plus g, which is fixed at this point) we can choose the h<sub>i</sub>’s in a greedy fashion: starting from h<sub>g</sub> working our way down to h<sub>0</sub>, try to choose h<sub>i</sub> to be as large as possible without having ∑<sub>i=0</sub><sup>g</sup> h<sub>i</sub>·m<sup>i</sup> exceeding v, with the exception that once the sum goes beyond u we should stop.",
"What remains is to be able to compare solutions to pick the lexicographically smallest shortest one, we’ll leave this to the reader.",
]),
("B", "Affine Mess", [
"There are four unknown parameters to determine: the matching of input points to output points, the rotation, the scaling, and the translation. There are at most 6 ways of matching the input points to the output points, and at most 80 different possibilities for the rotation, so we can simply try all of these.",
"Once the matching of points and rotation has been fixed, determining if there are valid scaling and translation parameters (and verifying their uniqueness) boils down to simple algebra.",
]),
("C", "Ancient Messages", [
"This problem may at first glance appear pretty difficult, but the key point is to note that all the different hieroglyphic shapes contain a different number of “holes”. This makes the problem one of the easiest: find the connected regions of the picture and then, for every black region R, count how many different white regions are adjacent to R (making sure to pad the entire picture with a white frame to make the outer region one single region).",
"A different, more fancy solution, is to use the Euler characteristic to compute the genus of each black region.",
]),
("D", "Chips Challenge", [
"This problem has a very distinct max flow smell, and indeed, flows are involved in the solution. First, suppose we think of the solution board as the adjacency matrix of a directed graph, with a component in row i column j being a unit of flow from i to j. Then, the constraint that there are equally many components in row i and column i just corresponds to each vertex having the same in-flow as out-flow. In other words, the solution is a circulation in a flow graph. To be specific, this flow graph is the graph on N vertices where there is capacity 1 from i to j if row i column j of the input board is not blocked. Furthermore, if we put cost 1 on those capacity 1 edges, the cost of the circulation precisely corresponds to the number of widgets used, so it seems hopeful that maximum cost circulations (which are perhaps less known than their cousins the min cost max flows, but can also be found efficiently) should be involved in the solution somehow.",
"However, there are two obstacles. First, there are some widgets that need to be used in the solution. This can be handled by either applying a lower bound on the flow of the corresponding edges (which makes finding an initial feasible solution a bit more complicated), or, more simply, by putting a large negative cost on these edges, heavily penalizing any solution that does not use them.",
"Second, there is the requirement that no row or column can contain more than an A/B fraction of all widgets. If this constraint was an absolute constraint, saying that at most m widgets can be placed on any row or column, it could easily be handled by introducing vertex capacities m in the graph (using the standard trick of splitting each vertex into an invertex and an out-vertex). Now, to handle the relative constraint, we can guess the value of m, solve the problem with that absolute bound, and check that the total number of widgets becomes at least m · B/A. There are at most N + 1 possible values of m so this only incurs an extra factor N in the running time (which in fact can be avoided by reusing the result for m − 1 when computing the maximum number of widgets for vertex capacities m).",
]),
("E", "Coffee Central", [
"To solve this problem, it is useful to mentally rotate the city by 45 degrees. The problem then (essentially) asks for the maximum array sum in a subarray. This is a well-known problem that has a simple O(n<sup>2</sup>) solution (per query), based on computing prefix sums. The details (hidden in the “essentially” above) end up being slightly messier: since the city grid is discrete you can’t really rotate it 45 degrees and apply the maximum array sum solution. Rather, you should translate the maximum array sum solution to the rotated case.",
]),
("F", "Machine Works", [
"This is a quite tricky problem. We’ll process the machines by order of availability date, and use a carefully built data structure to keep track of what our best options so far are. The data structure consists of a list of straight lines of the form M = c + kD for some constants c and k, indicating that at day D we can have M dollars. We keep this list pruned so that only lines that are the best possible for some day are actually present, and sorted by slope. For a given day D we can find the maximum amount of money for day D in logarithmic time (in C++ STL the most natural way of implementing this gives log-squared time but that’s OK).",
"When we process a new machine (with availability day D<sub>i</sub>), we compute the maximum amount of money available on day D<sub>i</sub>. Then, from any day after D<sub>i</sub>, a new line is possible by switching to machine i on day D<sub>i</sub>. (This new linear function is only valid from day D<sub>i</sub> and onwards, but as we’re processing the machines in order by availability day that’s ok.) We then need to add this new line to the list of available lines (and prune away lines that are no longer optimal at any point), which can also be done in logarithmic time.",
]),
("G", "Magic Sticks", [
"The first step is to figure out what to do in the case when all segments have to be used to form a single polygon. If one plays around with it a little bit, it is pretty natural to guess that in that case the best solution is to put all the vertices on a common circle. To figure out the exact placements of the sticks one then has to compute the radius of this circle. This can be done by a standard bisection search (i.e., real-valued binary search). Some care needs to be taken here, as there are two cases to consider (whether the center of the circle lies inside the polygon or not).",
"With the single-polygon solution as a toolkit, it is not very hard to solve the full problem, all that needs to be figured out is how to partition the sticks into groups. There is a straightforward O(n<sup>3</sup>) dynamic programming solution to this, but this is too slow. To make it fast enough, the key insight is the following: if we’re not using all the segments to form a single polygon, we should discard the longest segement. This leads to an O(n<sup>2</sup>) solution.",
]),
("H", "Mining Your Own Business", [
"This problem can be solved by finding the 2-vertex-connected components of the graph (or in other words, by the decomposition of the graph based on its articulation vertices). The set of 2-vertex-connected components form a tree, and it is easy to prove that it is necessary and sufficient to place an escape shaft in each leaf of this tree. The total number of ways in which this can be done is just the product of the sizes of the 2-vertex-connected components corresponding to those leafs.",
"There is a tricky border case to take care of, which is the case when the entire graph is 2-vertex-connected is a special case; then 2 escape shafts are needed (1 escape shaft is never sufficient since the junction of that single escape can collapse) and they can be placed in (<span style=\"display:inline-block;vertical-align:middle;text-align:center;line-height:1.1;font-size:0.9em\">V<span style=\"display:block\">2</span></span>) ways, where V is the number of vertices.",
]),
("I", "Mummy Madness", [
"There are two observations to make in this problem. The first, minor observation, is that the answer, if finite, is at most B (where B is the bound on the coordinates). This means that we can do a binary search for the longest possible survival time, answering “infinity” if it exceeds B.",
"To check if one can survive for T time steps, the main observation is that it suffices to check if there is some point that is reachable in T steps that no mummy can reach in T steps. This amounts to checking whether the union of n squares of side length 2T + 1 completely cover another square of side length 2T + 1. This can be done in n log n time using a standard sweepline approach.",
]),
("J", "Pyramids", [
"This problem is pretty much a standard knapsack problem. We can precompute a matrix back[k][N], indicating which pyramid to use if we have N cubes and are trying to produce a solution using k pyramids (or an indication that no such solution exists). This may seem like a huge matrix since N can be 10<sup>6</sup>, but one can easily check that, when there is a solution for N ≤ 10<sup>6</sup>, the smallest number of pyramids is at most 6, and the number of different pyramids is small. Then for every query N we find the smallest k such that back[k][N] is possible.",
"People who are more clever than me may also realize that the problem is also solvable brute force.",
]),
("K", "Trash Removal", [
"Despite being the only real computational geometry problem in an unusually geometry-free problem set, this problem is not too hard. Without loss of generality, one can assume that in an optimal solution there are two verties of the polygon touching one of the two sides of the trash chute, so we’ll try all such pairs of vertices and figure out the resulting chute width (which is easy).",
]),
]

def make_page(letter, title, paras):
    body = "\n\n".join("<p>%s</p>" % p for p in paras)
    return (
"<!DOCTYPE html>\n"
"<html lang=\"en\">\n"
"<head>\n"
"<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
"<title>Problem %s: %s (Solution) — %s</title>\n"
"<style>%s</style>\n"
"</head>\n"
"<body>\n"
"<p class=\"backlink\"><a href=\"index.html\">← All solutions</a></p>\n"
"\n"
"<header>\n"
"  <p class=\"kicker\">%s</p>\n"
"  <h1>Problem %s: %s</h1>\n"
"</header>\n"
"\n"
"%s\n"
"</body>\n"
"</html>\n"
    ) % (letter, title, COMP, css_page, COMP, letter, title, body)

# Write per-problem pages
for letter, title, paras in PROBLEMS:
    with open(os.path.join(SOL, letter + ".html"), "w", encoding="utf-8") as f:
        f.write(make_page(letter, title, paras))

# ---- Solutions index ----
rows = "\n".join(
'    <tr><td><a href="%s.html">%s</a></td><td class="title"><a href="%s.html">%s</a></td></tr>'
% (letter, letter, letter, title)
for letter, title, _ in PROBLEMS)

index_html = (
"<!DOCTYPE html>\n"
"<html lang=\"en\">\n"
"<head>\n"
"<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
"<title>Solution sketches — %s</title>\n"
"<style>%s</style>\n"
"</head>\n"
"<body>\n"
"<p class=\"backlink\"><a href=\"../problems/index.html\">← Problem set</a></p>\n"
"\n"
"<header>\n"
"  <p class=\"kicker\">%s</p>\n"
"  <h1>Solution sketches</h1>\n"
"  <p class=\"meta\">11 solutions (A–K)</p>\n"
"</header>\n"
"\n"
"<p><strong>Disclaimer</strong> This is an unofficial analysis of some possible ways to solve the problems of the ACM ICPC World Finals 2011. Any error in this text is my error. Should you find such an error, I would be happy to hear about it at austrin@kth.se.</p>\n"
"<p>Also, note that these sketches are just that—sketches. They are not intended to give a complete solution, but rather to outline some approach that can be used to solve the problem. If some of the terminology or algorithms mentioned below are not familiar to you, your favorite search engine should be able to help.</p>\n"
"<p>Finally, I want to stress that while I’m the one who has written this document, I do not take credit for the ideas behind these solutions—they come from many different people.</p>\n"
"<p>— Per Austrin</p>\n"
"\n"
"<table class=\"problems\">\n"
"  <tbody>\n"
"%s\n"
"  </tbody>\n"
"</table>\n"
"\n"
"<h2>Summary</h2>\n"
"\n"
"<p>A common theme that recurred in many of this year’s problems is guessing: guess a part of the answer, and then with this part fixed do some computations to see if the guess leads to a correct answer. (Of course, the details of exactly what to guess and how to figure out if the guess leads to an answer differs.) Problems where this applies are: A, B, D, I, and K.</p>\n"
"<p>Regarding the difficulties of the problem, my guesses were even more way off than usual. I had expected problem B to be the second easiest problem which turned out to be way off (never underestimate the deterring effect of a large mass of text...). Instead, the two easiest problems turned out to be C (which I did guess) and K (which I should have guessed but somehow did not). Almost all teams solved both of these. The next chunk of problems were E and J, both solved by slightly more than half of the teams. Continuing in the same pattern, problems A and H, were solved by roughly a third of the teams. The remaining problems were less popular, with at most 7 solutions for each. Problem D was the only one that was not solved.</p>\n"
"<p>Here are the stats of how many solutions there were<sup>1</sup>:</p>\n"
"\n"
"<table class=\"problems\">\n"
"<tr><td>Problem</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td><td>I</td><td>J</td><td>K</td></tr>\n"
"<tr><td>Submissions</td><td>138</td><td>36</td><td>192</td><td>12</td><td>223</td><td>33</td><td>107</td><td>195</td><td>10</td><td>396</td><td>297</td></tr>\n"
"<tr><td>Solved</td><td>35</td><td>7</td><td>98</td><td>0</td><td>63</td><td>2</td><td>7</td><td>39</td><td>2</td><td>60</td><td>94</td></tr>\n"
"</table>\n"
"\n"
"<p>As an additional curiosity fact: the judges were somewhat worried this year that some team would solve all 11 problems. We estimated roughly 4 hours of coding time to solve all problems. Of course, this does not take debugging time into account or the fact that it is almost impossible to utilize the computer at a 100%% efficiency. Turns out the problemset was more than hard enough, as usual.</p>\n"
"<p>Congratuliations to Zhejiang University for winning their first ICPC World Champions title!</p>\n"
"<p>1 Seven of the submissions to problem D were actually submissions to problem C.</p>\n"
"\n"
"<footer>\n"
"  © ICPC Foundation — solution sketches converted from the official PDF.\n"
"</footer>\n"
"</body>\n"
"</html>\n"
) % (COMP, css_index, COMP, rows)

with open(os.path.join(SOL, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("Wrote %d problem pages + index to %s" % (len(PROBLEMS), SOL))
for name in sorted(os.listdir(SOL)):
    print("  ", name)
