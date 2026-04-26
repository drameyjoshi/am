import sys

template = r"""\documentclass{article}
\usepackage{amsmath, amsthm, amsfonts, amssymb}
\theoremstyle{plain}
\newtheorem{thm}{Theorem}
\numberwithin{thm}{section}

\theoremstyle{plain}
\newtheorem{prop}{Proposition}
\numberwithin{prop}{section}

\theoremstyle{definition}
\newtheorem{defn}{Definition}
\numberwithin{defn}{section}

\theoremstyle{remark}
\newtheorem*{rem}{Remark}

\newtheorem*{cor}{Corollary}

\numberwithin{equation}{section}

\newcommand{\op}{\prime}
\begin{document}
\title{Choose title}
\author{Amey Joshi}
\maketitle
The document goes here.
\end{document}
"""

filename = sys.argv[1] if len(sys.argv) > 1 else "template.tex"
with open(filename, "w") as fw:
    print(template, file=fw)

