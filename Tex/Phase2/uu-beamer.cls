\ProvidesClass{uu-beamer}[Uppsala University Presentation Template v1.0]
\NeedsTeXFormat{LaTeX2e}

% Parent class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions \relax
\LoadClass{beamer}

% Set subtitles black
\usecolortheme[named=black]{structure}

%Font sizes
\setbeamerfont*{title}{size=\LARGE}
\setbeamerfont*{subtitle}{size=\normalsize}
\setbeamerfont{normal text}{size=\footnotesize}
\AtBeginDocument{\usebeamerfont{normal text}}

% Remove default logo
\logo{}

% Remove navigation bar
\beamertemplatenavigationsymbolsempty

% Background
\usepackage{tikz}

\usebackgroundtemplate{
    \begin{tikzpicture}[overlay,remember picture]
        % Background picture
        \node[at=(current page.north east),anchor=north east,inner sep=0pt,outer sep=0pt] {
            \includegraphics[keepaspectratio,height=0.4\paperheight]{uu_logo_bg}};

        % Logo
        \node[at=(current page.south east),anchor=south east,inner sep=0pt,outer sep=5mm] {
            \includegraphics[keepaspectratio,height=7mm]{uu_logo}};

    \end{tikzpicture}
}

% Letter spacing
\usepackage[letterspace=90]{microtype}

% Element margins
\setbeamerfont*{frametitle}{size=\Large} 
\setbeamertemplate{frametitle}[default][left,leftskip=1cm] % horizontal margin left
\addtobeamertemplate{frametitle}{\vskip+1cm \lsstyle}{} % vertical magin + letter spacing
\setbeamersize{text margin left=2cm}
\setbeamersize{text margin right=2cm}

% Uppercase titles
\newcommand{\Frametitle}[1]{\frametitle{\large \MakeUppercase{#1}}}

% Bullet lists
\setbeamertemplate{itemize items}[circle]

% Fonts 
\usepackage{mathptmx}
\usepackage{helvet}
%\usefonttheme{serif} % Uncomment to use Times-like font


%%%%%%%%%%%%%%%%%%%% Standard frames %%%%%%%%%%%%%%%%%%%

%______ Title page ______%
\defbeamertemplate*{title page}{customized}[1][]
{
    \begin{frame}
        \clearpage
        \vspace*{\fill}
        \begin{center}
            \usebeamerfont*{title} \textls[90]{\MakeUppercase{\inserttitle}}\par
            \vspace{15pt}
            \usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\textls[150]{\small \MakeUppercase{\insertsubtitle}}\par
        \end{center}
        \vfill
        \clearpage
    \end{frame}
}

%______ Logo page ______%
\newcommand{\logopage}{
    {
        \usebackgroundtemplate{
            \tikz[overlay,remember picture]
            \node[at=(current page.center),anchor=center,inner sep=0pt, inner sep=0] {
              \includegraphics[keepaspectratio,height=0.7\paperheight]{uu_logo}};
        }

        \begin{frame}[plain]
        \end{frame}
    }
}

%%%%%%%%%%%%%%%%%%%% Custom frames %%%%%%%%%%%%%%%%%%%

%______ Subtitle page ______%
\newcommand{\anothertitle}[2]
{
    \begin{frame}
        \clearpage
        \vspace*{\fill}
        \begin{center}
                \usebeamerfont*{title}{\textls[90]{\MakeUppercase{#1}}}\par
                \vspace{15pt}
                \usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\textls[150]{\small \MakeUppercase{#2}}\par
        \end{center}
        \vfill
        \clearpage
        \end{frame}
}

%______ Title + graphics + subtitle page ______%
\newcommand{\titleimage}[3]
{
    {
        \setbeamertemplate{frametitle}[default][center]
        \addtobeamertemplate{frametitle}{\vskip+1cm}{}

        \begin{frame}
            \frametitle[center]{\LARGE {\textls[90]{\MakeUppercase{#1}}}}

            \begin{center}
                \includegraphics<1>[height=4.5cm]{{#3}} \par
                \vspace{0.5cm}
                \scriptsize
                \textls[150]{\MakeUppercase{#2}}
            \end{center}
            
        \end{frame}
    }
}


%______ Fullsize image page ______%
\newcommand{\fullimage}[1]
{
    {
        \usebackgroundtemplate{
            \begin{tikzpicture}[overlay,remember picture]

                % Background logo
                \node[at=(current page.north east),anchor=north east,inner sep=0pt,outer sep=0pt] {
                    \includegraphics[keepaspectratio,height=0.4\paperheight]{uu_logo_bg}};
        
                % Image
                \node[at=(current page.center),anchor=center,inner sep=0pt,outer sep=0pt] {
                    \includegraphics[keepaspectratio,width=\paperwidth,height=\paperheight]{{#1}}};

                % Logo
                \node[at=(current page.south east),anchor=south east,inner sep=0pt,outer sep=5mm] {
                    \includegraphics[keepaspectratio,height=7mm]{uu_logo}};
            \end{tikzpicture}
        }
        \begin{frame}[plain]
        \end{frame}
    }
}