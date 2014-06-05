{% load i18n %}
{% load tags %}

\documentclass[%
    ngerman,  % Language setting for babel
]{scrartcl}

\usepackage{babel}  % Language setting see above
\usepackage[utf8]{inputenc}  % Encoding of source file
\usepackage[T1]{fontenc}  % Encoding of output file
\usepackage{textcomp}  % Special characters like euro character
\usepackage{libertine}  % font

\title{%
{% trans 'Protocol' %} {{ 'event_name'|get_config }}%
}

\date{%
{% if 'event_date'|get_config %}{{ 'event_date'|get_config }}{% else %}\today{% endif %}%
}

\begin{document}

\maketitle

\newpage

{% for item in items %}

\section*{%
{{ item }}%
}

{{ item.itemprotocol.protocol }}

{% endfor %}

\end{document}
