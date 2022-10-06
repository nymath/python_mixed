---
jupyter:
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.9.12
  latex_envs:
    autoclose: false
    autocomplete: true
    bibliofile: biblio.bib
    cite_by: apalike
    current_citInitial: 1
    eqLabelWithNumbers: true
    eqNumInitial: 1
    hotkeys:
      equation: Ctrl-E
      itemize: Ctrl-I
    labels_anchors: false
    LaTeX_envs_menu_present: true
    latex_user_defs: false
    report_style_numbering: false
    user_envs_cfg: false
  nbformat: 4
  nbformat_minor: 5
  nbTranslate:
    displayLangs:
    - \*
    hotkey: alt-t
    langInMainMenu: true
    sourceLang: en
    targetLang: fr
    useGoogleTranslate: true
  toc:
    base_numbering: 1
    nav_menu: {}
    number_sections: true
    sideBar: true
    skip_h1_title: false
    title_cell: Table of Contents
    title_sidebar: Contents
    toc_cell: false
    toc_position:
      height: calc(100% - 180px)
      left: 10px
      top: 150px
      width: 302.391px
    toc_section_display: true
    toc_window_display: true
  varInspector:
    cols:
      lenName: 16
      lenType: 16
      lenVar: 40
    kernels_config:
      python:
        delete_cmd_prefix: del
        library: var_list.py
        varRefreshCmd: print(var_dic_list())
      r:
        delete_cmd_postfix: )
        delete_cmd_prefix: rm(
        library: var_list.r
        varRefreshCmd: cat(var_dic_list())
    types_to_exclude:
    - module
    - function
    - builtin_function_or_method
    - instance
    - \_Feature
    window_display: false
---

::: {#3964f9c8 .cell .markdown}
本节尝试使用在jupyter
notebook使用zsh，顺便写一个zsh的食用指南，notebook写真的方便很多啊。
:::

::: {#2f391477 .cell .code execution_count="21" ExecuteTime="{\"start_time\":\"2022-09-30T07:52:44.443912Z\",\"end_time\":\"2022-09-30T07:52:44.456275Z\"}"}
``` python
import zsh_in_jupyter
```
:::

::: {#5198530e .cell .code}
``` python
```
:::

::: {#426de12e .cell .markdown}
# Introdution

因为及其好用，比如 具体而言 \\begin{itemize} \\item
许多功能在图形界面不提供，只有通过命令行来实现。 \\item Finder
会隐藏许多你不太会需要的文件，而 Command line 则可以访问所有文件。
\\item Command line 可以通过 SSH 远程访问你的 Mac 或者 Linux。 \\item
普通用户可以通过 `sudo` 命令获得 root 用户权限。 \\item
如果你开启手动输入用户名登陆模式，登陆时在用户名处输入 `>console`
可以直接进入命令行界面。随后你仍然需要登录到一个账户。 \\end{itemize}
:::

::: {#37695442 .cell .code execution_count="31" ExecuteTime="{\"start_time\":\"2022-09-30T00:56:16.236101Z\",\"end_time\":\"2022-09-30T00:56:16.384245Z\"}"}
``` python
!echo ~
```

::: {.output .stream .stdout}
    /Users/nymath
:::
:::

::: {#a302ba1e .cell .code execution_count="45" ExecuteTime="{\"start_time\":\"2022-09-30T01:22:17.531868Z\",\"end_time\":\"2022-09-30T01:22:17.678779Z\"}"}
``` python
get_ipython().system('echo ~')
```

::: {.output .stream .stdout}
    /Users/nymath
:::
:::

::: {#a524a580 .cell .code execution_count="3" ExecuteTime="{\"start_time\":\"2022-09-30T07:18:04.628601Z\",\"end_time\":\"2022-09-30T07:18:04.912812Z\"}"}
``` python
# 打开当前文件夹
!temp=$(pwd);\
open $temp
```
:::

::: {#4831e23d .cell .code execution_count="93" ExecuteTime="{\"start_time\":\"2022-09-30T01:36:53.185536Z\",\"end_time\":\"2022-09-30T01:36:53.195705Z\"}" code_folding="[]"}
``` python
def zsh(par='temp=$(pwd);open $temp'):
    if type(par) == str:
        return get_ipython().system(par)
    else:
        return 'type error'
```
:::

::: {#ca8dc0b8 .cell .code execution_count="55" ExecuteTime="{\"start_time\":\"2022-09-30T01:24:40.391320Z\",\"end_time\":\"2022-09-30T01:24:40.623978Z\"}"}
``` python
func.system('temp=$(pwd);open $temp')
```
:::

::: {#f017b2d9 .cell .code execution_count="52" ExecuteTime="{\"start_time\":\"2022-09-30T01:23:49.320447Z\",\"end_time\":\"2022-09-30T01:23:49.583670Z\"}"}
``` python
get_ipython().system('temp=$(pwd);open $temp')
```
:::

::: {#ce7fec45 .cell .code}
``` python
from zsh_in_jupyter import 
```
:::

::: {#d9c1184a .cell .markdown}
## Terminlogy

-   **Command line**: A command-line interface is a way of giving
    instructions to a computer and getting results back
-   **Shell**: A shell is a program that creates a user interface of one
    kind or another enabling you to interact with a computer
    -   **csh**: the C shell, named for similarities to the C
        programming language
    -   **zsh**: the Z shell, an advanced shell named after Yale
        professor Zhong Shao that incorporates features from tcsh, ksh,
        and bash, plus other capabilities
    -   **dash**: the Debian Almquist shell, a lightweight shell that's
        been around for more than two decades, but was not included with
        macOS until Catalina
-   **Terminal**: the devices people used to interact with computers
    back in the days of monolithic mainframes.
:::

::: {#1f3f48b1 .cell .markdown}
:::

::: {#8cde7b83 .cell .markdown}
## commands, aruguments and flags

-   **Command**: Commands are straightforward; they're the verbs of the
    command line (eventhough they may look nothing like English verbs).

```{=html}
<!-- -->
```
    pwd
    date

-   **Arguments**: Along with commands (verbs), we have arguments, which
    you can think ofas nouns

比如你要处理一个文件，需要指定这个文件的名字

    nano file1

-   **Flags**: Besides verbs and nouns, we have adverbs! In English, I
    could say, "Eatcereal quickly!" or "Watch TV quietly."

ls展示文件，ls a展示所有文件
:::

::: {#4d64b54c .cell .code execution_count="2" ExecuteTime="{\"start_time\":\"2022-09-29T16:41:43.688813Z\",\"end_time\":\"2022-09-29T16:41:43.839785Z\"}"}
``` python
!pwd; \
date
```

::: {.output .stream .stdout}
    /Users/nymath/Desktop/python/python_quant/Statistical_learning
    Fri Sep 30 00:41:43 CST 2022
:::
:::

::: {#ecc4840a .cell .code execution_count="26" ExecuteTime="{\"start_time\":\"2022-09-29T16:50:45.309923Z\",\"end_time\":\"2022-09-29T16:50:45.462577Z\"}"}
``` python
!ls -l -a
```

::: {.output .stream .stdout}
    total 88
    drwxrwxr-x@  7 nymath  staff    224 Sep 30 00:49 .
    drwxr-xr-x@ 16 nymath  staff    512 Sep 30 00:35 ..
    drwxr-xr-x   4 nymath  staff    128 Sep 29 21:14 .ipynb_checkpoints
    -rw-r--r--   1 nymath  staff  22692 Sep 30 00:22 Structures of Data.ipynb
    -rw-r--r--@  1 nymath  staff    158 Sep 30 00:22 fib.py
    -rw-------   1 nymath  staff    170 Sep 30 00:12 fib.py.save
    -rw-r--r--   1 nymath  staff  11053 Sep 30 00:49 zsh_basics.ipynb
:::
:::

::: {#0e93f1a0 .cell .code execution_count="5" ExecuteTime="{\"start_time\":\"2022-09-29T16:42:50.945098Z\",\"end_time\":\"2022-09-29T16:42:51.094768Z\"}"}
``` python
!ls -a; #
```

::: {.output .stream .stdout}
    .                        Structures of Data.ipynb zsh_basics.ipynb
    ..                       fib.py
    .ipynb_checkpoints       fib.py.save
:::
:::

::: {#2b2a76af .cell .code execution_count="12" ExecuteTime="{\"start_time\":\"2022-09-29T16:44:15.544629Z\",\"end_time\":\"2022-09-29T16:44:15.695850Z\"}"}
``` python
!ls -a f* # show you only the names of files beginning with the letter f
```

::: {.output .stream .stdout}
    fib.py      fib.py.save
:::
:::

::: {#84684b9b .cell .code}
``` python
```
:::

::: {#af360aad .cell .markdown}
# Examples
:::

::: {#9de924ca .cell .markdown}
## open

open
命令用于打开一个文件夹或者具体的文件，如果指定的是applications中的.app文件，则可以直接打开。
:::

::: {#174159de .cell .code execution_count="15" ExecuteTime="{\"start_time\":\"2022-09-30T07:42:34.767907Z\",\"end_time\":\"2022-09-30T07:42:35.005213Z\"}"}
``` python
!open /Applications/Notability.app 
```
:::

::: {#025763cf .cell .code execution_count="16" ExecuteTime="{\"start_time\":\"2022-09-30T07:42:52.079154Z\",\"end_time\":\"2022-09-30T07:42:52.279502Z\"}"}
``` python
!open /Applications/Safari.app
```
:::

::: {#81284268 .cell .code execution_count="17" ExecuteTime="{\"start_time\":\"2022-09-30T07:43:34.869178Z\",\"end_time\":\"2022-09-30T07:43:35.078908Z\"}"}
``` python
!open /Applications/WeChat.app
```
:::

::: {#cc31e69f .cell .code execution_count="18" ExecuteTime="{\"start_time\":\"2022-09-30T07:44:46.777129Z\",\"end_time\":\"2022-09-30T07:44:47.039387Z\"}"}
``` python
!temp=$(pwd);\
open $temp
```
:::

::: {#144151c5 .cell .markdown}
## find & which {#find--which}

We can type the command \"find\" to find the files whose name contains
the name given by input. To be specific, if we want to find
site-packages in /opt/, we can
:::

::: {#e45b3c74 .cell .code execution_count="5" ExecuteTime="{\"start_time\":\"2022-09-30T07:35:31.920231Z\",\"end_time\":\"2022-09-30T07:35:32.868986Z\"}"}
``` python
!find /opt/anaconda3/lib/python3.9 -name "*site-packages*"
```

::: {.output .stream .stdout}
    /opt/anaconda3/lib/python3.9/site-packages
:::
:::

::: {#8350374f .cell .code execution_count="29" ExecuteTime="{\"start_time\":\"2022-09-30T15:08:33.189885Z\",\"end_time\":\"2022-09-30T15:08:37.267177Z\"}"}
``` python
!find /opt/anaconda3 -name "nbconvert"
```

::: {.output .stream .stdout}
    /opt/anaconda3/pkgs/jupyter_server-1.13.5-pyhd3eb1b0_0/site-packages/jupyter_server/tests/nbconvert
    /opt/anaconda3/pkgs/jupyter_server-1.13.5-pyhd3eb1b0_0/site-packages/jupyter_server/tests/services/nbconvert
    /opt/anaconda3/pkgs/jupyter_server-1.13.5-pyhd3eb1b0_0/site-packages/jupyter_server/nbconvert
    /opt/anaconda3/pkgs/jupyter_server-1.13.5-pyhd3eb1b0_0/site-packages/jupyter_server/services/nbconvert
    /opt/anaconda3/pkgs/notebook-6.4.8-py39hecd8cb5_0/lib/python3.9/site-packages/notebook/nbconvert
    /opt/anaconda3/pkgs/notebook-6.4.8-py39hecd8cb5_0/lib/python3.9/site-packages/notebook/services/nbconvert
    /opt/anaconda3/pkgs/nbconvert-6.4.4-py39hecd8cb5_0/info/test/nbconvert
    /opt/anaconda3/pkgs/nbconvert-6.4.4-py39hecd8cb5_0/lib/python3.9/site-packages/nbconvert
    /opt/anaconda3/pkgs/nbconvert-6.4.4-py39hecd8cb5_0/share/jupyter/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/jupyter_server/tests/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/jupyter_server/tests/services/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/jupyter_server/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/jupyter_server/services/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/notebook/nbconvert
    /opt/anaconda3/lib/python3.9/site-packages/notebook/services/nbconvert
    /opt/anaconda3/share/jupyter/nbconvert
:::
:::

::: {#b6ded64b .cell .code execution_count="33" ExecuteTime="{\"start_time\":\"2022-09-30T15:19:19.015042Z\",\"end_time\":\"2022-09-30T15:19:27.494475Z\"}"}
``` python
!find /Users/ -name "pandoc"
```

::: {.output .stream .stdout}
    /Users//nymath/Library/TeXShop/Engines/Inactive/pandoc
:::
:::

::: {#87591abe .cell .code execution_count="14" ExecuteTime="{\"start_time\":\"2022-09-30T07:40:14.559020Z\",\"end_time\":\"2022-09-30T07:40:14.710439Z\"}"}
``` python
!which jupyter
```

::: {.output .stream .stdout}
    /opt/anaconda3/bin/jupyter
:::
:::

::: {#291f956f .cell .code execution_count="13" ExecuteTime="{\"start_time\":\"2022-09-30T07:39:29.925982Z\",\"end_time\":\"2022-09-30T07:39:30.072130Z\"}"}
``` python
!which python # python解释器所在位置，的确是vscode中用到的那个。
```

::: {.output .stream .stdout}
    /opt/anaconda3/bin/python
:::
:::

::: {#ffb615b4 .cell .code}
``` python
```
:::

::: {#a39c071a .cell .markdown}
## Pandoc
:::

::: {#b09c3138 .cell .code execution_count="34" ExecuteTime="{\"start_time\":\"2022-09-30T15:19:57.214660Z\",\"end_time\":\"2022-09-30T15:20:05.194696Z\"}"}
``` python
# 获取pandoc的安装路径
!find /Users -name "pandoc"
```

::: {.output .stream .stdout}
    /Users/nymath/Library/TeXShop/Engines/Inactive/pandoc
:::
:::

::: {#fbe638fc .cell .code execution_count="36" ExecuteTime="{\"start_time\":\"2022-09-30T15:20:23.358267Z\",\"end_time\":\"2022-09-30T15:20:23.597120Z\"}"}
``` python
!open /Users/nymath/Library/TeXShop/Engines/Inactive/pandoc
```
:::

::: {#e4630bd7 .cell .code execution_count="37" ExecuteTime="{\"start_time\":\"2022-09-30T15:20:42.905314Z\",\"end_time\":\"2022-09-30T15:20:43.044110Z\"}"}
``` python
# pandoc这个解释器?或者说函数？命令？保存的位置
!which pandoc
```

::: {.output .stream .stdout}
    /usr/local/bin/pandoc
:::
:::

::: {#2a90969a .cell .markdown}
开始pandoc的应用介绍了
:::

::: {#473c0246 .cell .code execution_count="49" ExecuteTime="{\"start_time\":\"2022-09-30T15:39:50.206805Z\",\"end_time\":\"2022-09-30T15:39:50.385520Z\"}"}
``` python
!pandoc --version
```

::: {.output .stream .stdout}
    pandoc 2.19.2
    Compiled with pandoc-types 1.22.2.1, texmath 0.12.5.2, skylighting 0.13,
    citeproc 0.8.0.1, ipynb 0.2, hslua 2.2.1
    Scripting engine: Lua 5.4
    User data directory: /Users/nymath/.local/share/pandoc
    Copyright (C) 2006-2022 John MacFarlane. Web:  https://pandoc.org
    This is free software; see the source for copying conditions. There is no
    warranty, not even for merchantability or fitness for a particular purpose.
:::
:::

::: {#f785618a .cell .code execution_count="40" ExecuteTime="{\"start_time\":\"2022-09-30T15:24:04.973009Z\",\"end_time\":\"2022-09-30T15:24:05.126209Z\"}"}
``` python
!mkdir pandoc-test
```
:::

::: {#e30959f9 .cell .code execution_count="45" ExecuteTime="{\"start_time\":\"2022-09-30T15:25:10.156960Z\",\"end_time\":\"2022-09-30T15:25:10.304545Z\"}"}
``` python
!cd pandoc-test;\
pwd;\
```

::: {.output .stream .stdout}
    /Users/nymath/Desktop/python/python_quant/Statistical_learning/pandoc-test
:::
:::

::: {#c3ea2f9f .cell .markdown}
相关命令解读

``` {zsh}
pandoc test1.md -f markdown -t html -s -o test1.html
```

*test1.md* tells pandoc which file to convert.\
*-f* markdown -t html: from md to html.\
*-s* says to create a "standalone" file\
*-o* test1.html says to put the output in the file test1.html.
:::

::: {#6c419ee4 .cell .markdown}
    pandoc -f html -t markdown hello.html

将hello.html转化为hello.md
:::

::: {#9abc7771 .cell .code ExecuteTime="{\"start_time\":\"2022-09-30T15:44:23.910Z\"}"}
``` python
!pandoc zsh_basics.ipynb -f ipynb -t pdf -s -o zsh_basics.pdf
```
:::

::: {#b2979229 .cell .code execution_count="41" ExecuteTime="{\"start_time\":\"2022-09-30T15:24:19.491691Z\",\"end_time\":\"2022-09-30T15:24:19.751716Z\"}"}
``` python
zsh_in_jupyter.opendir()
```
:::

::: {#65e21385 .cell .code}
``` python
```
:::

::: {#7561f4c2 .cell .code}
``` python
```
:::

::: {#fd70abf2 .cell .code}
``` python
```
:::

::: {#f878e023 .cell .code}
``` python
```
:::

::: {#9c49f921 .cell .code}
``` python
```
:::

::: {#beded58d .cell .code}
``` python
```
:::

::: {#54253909 .cell .markdown}
## nbconvert
:::

::: {#9f9996d8 .cell .markdown}
[指南](https://nbconvert.readthedocs.io/en/latest/usage.html?highlight=pdf)\
当然pandoc也非常重要，可以看看\
[Pandoc](https://pandoc.org/)
:::

::: {#d472e0de .cell .markdown}
### HTML
:::

::: {#840690bf .cell .code execution_count="36" ExecuteTime="{\"start_time\":\"2022-09-30T01:01:14.331950Z\",\"end_time\":\"2022-09-30T01:01:15.963556Z\"}"}
``` python
# HTML
!jupyter nbconvert --to html zsh_basics.ipynb
```

::: {.output .stream .stdout}
    [NbConvertApp] Converting notebook zsh_basics.ipynb to html
    [NbConvertApp] Writing 595565 bytes to zsh_basics.html
:::
:::

::: {#87d51d83 .cell .markdown ExecuteTime="{\"start_time\":\"2022-09-30T01:11:00.613532Z\",\"end_time\":\"2022-09-30T01:11:00.621131Z\"}"}
### PDF

PDF转化为pdf倒是挺费功夫的，不信的话直接转化看看，应该会报错，比如不支持中文，因此我们需要去弄一个template\
这个文件所在路径为/opt/anaconda3/share/jupyter/nbconvert/templates/latex
:::

::: {#8c8f166b .cell .code execution_count="30" ExecuteTime="{\"start_time\":\"2022-09-30T15:09:48.146641Z\",\"end_time\":\"2022-09-30T15:09:48.378985Z\"}"}
``` python
!open /opt/anaconda3/share/jupyter/nbconvert/templates/latex 
```
:::

::: {#06137370 .cell .code execution_count="28" ExecuteTime="{\"start_time\":\"2022-09-30T15:06:43.279687Z\",\"end_time\":\"2022-09-30T15:06:51.031069Z\"}"}
``` python
!jupyter nbconvert --to pdf zsh_basics.ipynb
```

::: {.output .stream .stdout}
    [NbConvertApp] Converting notebook zsh_basics.ipynb to pdf
    [NbConvertApp] Writing 48048 bytes to zsh_basics.pdf
:::
:::

::: {#62e24bad .cell .code}
``` python
!jupyter nbconvert --to pdf --template custom_template.tplx zsh_basics.ipynb
```
:::

::: {#7ff6fb22 .cell .code}
``` python
```
:::

::: {#d9b2b500 .cell .markdown}
### Python
:::

::: {#56272e70 .cell .code execution_count="26" ExecuteTime="{\"start_time\":\"2022-09-30T15:05:38.435076Z\",\"end_time\":\"2022-09-30T15:05:40.136614Z\"}"}
``` python
!jupyter nbconvert --to python zsh_basics.ipynb
```

::: {.output .stream .stdout}
    [NbConvertApp] Converting notebook zsh_basics.ipynb to python
    [NbConvertApp] Writing 4870 bytes to zsh_basics.py
:::
:::

::: {#09bc2ee6 .cell .code execution_count="98" ExecuteTime="{\"start_time\":\"2022-09-30T01:56:27.739231Z\",\"end_time\":\"2022-09-30T01:56:28.004862Z\"}"}
``` python
zsh()
```
:::

::: {#bad748bc .cell .markdown}
### Latex
:::

::: {#b9528858 .cell .code execution_count="96" ExecuteTime="{\"start_time\":\"2022-09-30T01:48:01.831826Z\",\"end_time\":\"2022-09-30T01:48:04.487723Z\"}"}
``` python
!jupyter nbconvert --to latex zsh_basics.ipynb
```

::: {.output .stream .stdout}
    [NbConvertApp] Converting notebook zsh_basics.ipynb to latex
    [NbConvertApp] Writing 31753 bytes to zsh_basics.tex
:::
:::

::: {#35a6ca5c .cell .markdown}
修改 documentclass\[11pt\]{article}\
为\
documentclass{article}\
usepackage{ctex}
:::

::: {#1c7d164c .cell .code execution_count="1" ExecuteTime="{\"start_time\":\"2022-09-30T03:32:23.108308Z\",\"end_time\":\"2022-09-30T03:32:23.118412Z\"}"}
``` python
import zsh_in_jupyter
```
:::

::: {#6567a6f4 .cell .code execution_count="5" ExecuteTime="{\"start_time\":\"2022-09-30T07:23:38.587480Z\",\"end_time\":\"2022-09-30T07:23:38.593597Z\"}"}
``` python
# 查看模组的说明
print(zsh_in_jupyter.__doc__)
```

::: {.output .stream .stdout}

    用于调用xxx
:::
:::

::: {#8400b0b0 .cell .code execution_count="6" ExecuteTime="{\"start_time\":\"2022-09-30T07:23:40.737537Z\",\"end_time\":\"2022-09-30T07:23:41.002374Z\"}"}
``` python
zsh_in_jupyter.opendir()
```
:::

::: {#26e90691 .cell .code}
``` python
!open 
```
:::

::: {#2c6881f1 .cell .code}
``` python
```
:::

::: {#5de6e2f3 .cell .code}
``` python
```
:::

::: {#4ce8b5a7 .cell .markdown}
# Work with Files and Directories

似乎用的不太多，但还是写一点
:::

::: {#fee21310 .cell .markdown}
## Create a File

Command **touch** is used for creating a file. (md
macos简直了，右键创建文件夹都得付费)
:::

::: {#fe2faaec .cell .code execution_count="19" ExecuteTime="{\"start_time\":\"2022-09-30T07:52:20.300681Z\",\"end_time\":\"2022-09-30T07:52:20.475020Z\"}"}
``` python
!touch test.sh
```
:::

::: {#22504561 .cell .code execution_count="24" ExecuteTime="{\"start_time\":\"2022-09-30T07:56:07.866789Z\",\"end_time\":\"2022-09-30T07:56:08.152377Z\"}"}
``` python
zsh_in_jupyter.opendir()
```
:::

::: {#989345a2 .cell .markdown}
## Create a Directory
:::

::: {#2cf3ca8f .cell .code}
``` python
```
:::

::: {#bc0b18fa .cell .code}
``` python
```
:::

::: {#bc02dd51 .cell .code}
``` python
```
:::

::: {#d7e05175 .cell .code}
``` python
```
:::

::: {#4665e0f1 .cell .code}
``` python
```
:::

::: {#c414eefd .cell .code}
``` python
```
:::

::: {#a7292b00 .cell .code}
``` python
```
:::

::: {#6f626e67 .cell .code}
``` python
```
:::

::: {#71771c75 .cell .code}
``` python
```
:::

::: {#87afa687 .cell .code}
``` python
```
:::

::: {#50f27d9c .cell .code}
``` python
```
:::

::: {#800ab4ea .cell .code}
``` python
```
:::
