{% load tags %}

\documentclass[%
    ngerman,  % Spracheinstellung für babel
]{scrartcl}

\usepackage{babel}  % Spracheinstellung als Klassenoption oben
\usepackage[utf8]{inputenc}  % Kodierung der Quelldatei
\usepackage[T1]{fontenc}  % Ausgabekodierung
\usepackage{textcomp}  % Sonderzeichen z. B. Euro-Zeichen
\usepackage{ulem} \normalem  % Unterstreichen mit \uline{} möglich
\usepackage{libertine}  % Schriftart

\title{
{{ 'event_name'|get_config }}
}

\date{
{% if 'event_date'|get_config %}{{ 'event_date'|get_config }}{% else %}\today{% endif %}
}

\begin{document}

\maketitle

{% for item in items %}

\section*{
{{ item }}
}

{{ item.itemprotocol.protocol }}

{% endfor %}

\end{document}
