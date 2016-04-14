% asg.cls Anna Koop, 2016
%
% Anna's style file for making assignments.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{asg}[2016/04/11 version 0.8 Assignments the way I want them.]

% default to article unless a file specifies otherwise
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions \relax

% basing everything on the article class unless overridden
\LoadClass{article}



%%%%%%%%%%%%%%%%%%%
%%  Eternally useful PACKAGES
%%%%%%%%%%%%%%%%%%%

%latexsym,setspace}
% RequirePackage rather than usepackage so this can come before \documentclass
\RequirePackage{natbib}

\RequirePackage{amsfonts,amsmath,amsthm}
\RequirePackage{url}
\RequirePackage{graphicx}
\RequirePackage{listings} % Required for insertion of code

\RequirePackage{array}
\RequirePackage{multicol} % for creating columns for readable text-blocks
\RequirePackage{multirow} % nifty tabular options
\RequirePackage{tabulary} % nice word cells

\RequirePackage{pdflscape} % for very large figures and rubrics

\RequirePackage{pgffor} %because foreach is handy
\RequirePackage{suffix} % because I want to have * versions of commands

%\usepackage{palatino}
%\usepackage{utopia}
%\usepackage{lmodern}
%\usepackage{txfonts}
%\RequirePackage{libertine}

\RequirePackage[margin=2.5cm]{geometry} % override width, sacrificing readability for writable space
\RequirePackage{fancyhdr} % for custom headers
\RequirePackage{lastpage} % for N of M page nubering
\RequirePackage{titling} % for keeping around author info, etc for headings
\RequirePackage{titlesec} % for readable customization of section spacing
\RequirePackage{enumitem} % compact lists

%%%%%%%%%%%%%%%%%%%
%%  VARIABLES
%%%%%%%%%%%%%%%%%%%
\def\Class#1{\def\@Class{#1}}
\def\ClassTitle#1{\def\@ClassTitle{#1}}
\def\Instructor#1{\def\@Instructor{#1}}
\def\Campus#1{\def\@Campus{#1}}
\def\Department#1{\def\@Department{#1}}
\def\Email#1{\def\@Email{#1}}
\def\Office#1{\def\@Office{#1}}
\def\Term#1{\def\@Term{#1}}
\def\Submission#1{\def\@Submission{#1}}

% set defaults
\Instructor{Prof}
\Office{404 HQ}
\Email{}
\Class{AUXXX XXX}
\ClassTitle{Introduction to \LaTeX}
\Campus{Augustana}
\Department{Department of Science}
\Term{Winter 2016}
\Submission{Submit via {\em eclass}}

% asg specific info
\def\Version#1{\def\@Version{#1}}
\def\AsgTitle#1{\def\@AsgTitle{#1}}
\def\AsgNum#1{\def\@AsgNum{#1}}
\def\Due#1{\def\@Due{#1}}
\def\Total#1{\def\@Total{#1}}

\Version{1.0}
\AsgTitle{Getting Started with \LaTeX}
\AsgNum{0}
\Due{Never}
\Total{0}


% Number questions
\newtheorem{definition}{Definition}[section]
\newtheorem{question}{Question}[section]


%%%%%%%%%%%%%%%%%%%
%%  LAYOUT
%%%%%%%%%%%%%%%%%%%

%% Typesetting preferences - HT Christophe http://tex.stackexchange.com/questions/59702/
\widowpenalty = 4000        % help suppress widows
\clubpenalty  = 4000        % help suppress orphans,
% from 0 to 10 000 (from 300 to 1 000 recommended, 10 000 not recommended)

%%%%%%%%%%%%%%%%%%%
%%  TITLE changes
%%%%%%%%%%%%%%%%%%%

\renewcommand{\maketitle}{ % Customize the title display
	{\LARGE{\bf Assignment \@AsgNum}: \@AsgTitle }\\
	\vspace*{1\baselineskip}
	
	\hrule
	
	\vspace*{0.75\baselineskip}

	\noindent
	{\bf Due}: {\em \@Due}\\
	{\bf Worth}: \@Total\% of final grade \\
	{\bf Instructor}: \@Instructor, \@Office, \@Email \\
	{\bf Submission Insructions}: \@Submission

	\vspace*{0.75\baselineskip}

	\hrule
	\vspace*{1.2\baselineskip}
	%\noindent
	%{\bf Note}
	%Please submit your assignment through eclass. Some questions require you to write small programs,
	%however for the written questions please format your answers
	%in a single {\em pdf\/} file.
	%Submit all required documents in a zip or tar archive.
	%\vspace*{1\baselineskip}

	\thispagestyle{front}
} % end title


% because of the enumitem package
\newlist{checklist}{itemize}{2} 
\setlist[checklist]{label=$\square$,noitemsep, topsep=0pt, before={\vspace*{-\baselineskip}}}

\newlist{writelist}{itemize}{2}
\setlist[writelist]{label=$\bullet$, topsep=\baselineskip,itemsep=\baselineskip}

%%%%%%%%%%%%%%%%%%%
%%  GENERAL SPACING
%%%%%%%%%%%%%%%%%%%

\parindent 0pt
\marginparwidth 0pt
\renewcommand{\baselinestretch}{1.2}

% thanks, enumitem package
\newlist{compactlist}{itemize}{4} 
\setlist[compactlist]{label=$\cdot$,noitemsep, topsep=0pt}%, before={\vspace*{-\baselineskip}}}


\titlespacing{\subsection}{0pt}{1em plus .1em minus .2em}{.4em plus .1em minus .1em} %{command}{left}{before}{after}

%%%%%%%%%%%%%%%%%%%
%%  HEADERS and FOOTERS
%%%%%%%%%%%%%%%%%%%
\newcommand{\nofm}{\thepage~of \pageref{LastPage}}  % due to lastpage package

\fancypagestyle{front}{%
 	\fancyhf{}
	\fancyhead[L]{\large\@Class}
	\fancyhead[R]{\large\@ClassTitle}
	\fancyfoot[L]{\@Campus}
	\fancyfoot[C]{\@Term}
	\fancyfoot[R]{\nofm}
	\renewcommand{\footrulewidth}{.5pt}
	\renewcommand{\headrulewidth}{0pt}
}%


\pagestyle{fancy} % due to fancyhdr package
\rfoot{\nofm} 
\lfoot{\@Campus}
\cfoot{\@Term}
\rhead{\@Class}
\lhead{\@title}
\renewcommand{\footrulewidth}{.5pt}
\renewcommand{\headrulewidth}{.5pt}


\endinput
