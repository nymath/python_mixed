#!/usr/bin/env python
# coding: utf-8

# 本节尝试使用在jupyter notebook使用zsh，顺便写一个zsh的食用指南，notebook写真的方便很多啊。

# In[21]:


import zsh_in_jupyter


# In[ ]:





# # Introdution
# 因为及其好用，比如
# 具体而言
# \begin{itemize}
# \item 许多功能在图形界面不提供，只有通过命令行来实现。
# \item Finder 会隐藏许多你不太会需要的文件，而 Command line 则可以访问所有文件。
# \item Command line 可以通过 SSH 远程访问你的 Mac 或者 Linux。
# \item 普通用户可以通过 `sudo` 命令获得 root 用户权限。
# \item 如果你开启手动输入用户名登陆模式，登陆时在用户名处输入 `>console` 可以直接进入命令行界面。随后你仍然需要登录到一个账户。
# \end{itemize}
# 

# In[31]:


get_ipython().system('echo ~')


# In[45]:


get_ipython().system('echo ~')


# In[3]:


# 打开当前文件夹
get_ipython().system('temp=$(pwd);open $temp')


# In[93]:


def zsh(par='temp=$(pwd);open $temp'):
    if type(par) == str:
        return get_ipython().system(par)
    else:
        return 'type error'


# In[55]:


func.system('temp=$(pwd);open $temp')


# In[52]:


get_ipython().system('temp=$(pwd);open $temp')


# In[ ]:


from zsh_in_jupyter import 


# ## Terminlogy
# - **Command line**: A command-line interface is a way of giving instructions to a computer and getting results back
# - **Shell**: A shell is a program that creates a user interface of one kind or another enabling you to interact with a computer
# 	- **csh**: the C shell, named for similarities to the C programming language
# 	- **zsh**: the Z shell, an advanced shell named after Yale professor Zhong
# 	Shao that incorporates features from tcsh, ksh, and bash, plus other
# 	capabilities
# 	- **dash**: the Debian Almquist shell, a lightweight shell that’s been around
# 	for more than two decades, but was not included with macOS until
# 	Catalina
# - **Terminal**: the devices people used to interact with computers back in the days of
# monolithic mainframes.

# 

# ## commands, aruguments  and flags
# 
# - **Command**: Commands are straightforward; they’re the verbs of the command line (eventhough they may look nothing like English verbs).
# ```
# pwd
# date
# ```
# - **Arguments**: Along with commands (verbs), we have arguments, which you can think ofas nouns
# 
# 比如你要处理一个文件，需要指定这个文件的名字
# 
# ```
# nano file1
# ```
# 
# - **Flags**: Besides verbs and nouns, we have adverbs! In English, I could say, “Eatcereal quickly!” or “Watch TV quietly.”
# 
# ls展示文件，ls a展示所有文件

# In[2]:


get_ipython().system('pwd; date')


# In[26]:


get_ipython().system('ls -l -a')


# In[5]:


get_ipython().system('ls -a; #')


# In[12]:


get_ipython().system('ls -a f* # show you only the names of files beginning with the letter f')


# In[ ]:





# # Examples

# ## open
# open 命令用于打开一个文件夹或者具体的文件，如果指定的是applications中的.app文件，则可以直接打开。

# In[15]:


get_ipython().system('open /Applications/Notability.app ')


# In[16]:


get_ipython().system('open /Applications/Safari.app')


# In[17]:


get_ipython().system('open /Applications/WeChat.app')


# In[18]:


get_ipython().system('temp=$(pwd);open $temp')


# ## find & which
# We can type the command "find" to find the files whose name contains the name given by input. To be specific, if we want to find site-packages in /opt/, we can 

# In[5]:


get_ipython().system('find /opt/anaconda3/lib/python3.9 -name "*site-packages*"')


# In[9]:


get_ipython().system('find /opt/anaconda3 -name "jupyter"')


# In[14]:


get_ipython().system('which jupyter')


# In[13]:


get_ipython().system('which python # python解释器所在位置，的确是vscode中用到的那个。')


# In[ ]:





# ## nbconvert

# ### HTML

# In[36]:


# HTML
get_ipython().system('jupyter nbconvert --to html zsh_basics.ipynb')


# ### PDF
# PDF转化为pdf倒是挺费功夫的，不信的话直接转化看看，应该会报错，比如不支持中文，因此我们需要去弄一个template  
# 这个文件所在路径为/opt/anaconda3/share/jupyter/nbconvert/templates/latex 

# In[41]:


get_ipython().system('open /opt/anaconda3/share/jupyter/nbconvert/templates/latex ')


# In[37]:


get_ipython().system('jupyter nbconvert --to pdf zsh_basics.ipynb')


# In[ ]:


get_ipython().system('jupyter nbconvert --to pdf --template custom_template.tplx zsh_basics.ipynb')


# ### Python

# In[25]:


get_ipython().system('jupyter nbconvert --to python zsh_basics.ipynb')


# In[98]:


zsh()


# ### Latex

# In[96]:


get_ipython().system('jupyter nbconvert --to latex zsh_basics.ipynb')


# 修改
# documentclass[11pt]{article}  
# 为   
# documentclass{article}   
# usepackage{ctex}  

# In[1]:


import zsh_in_jupyter


# In[5]:


# 查看模组的说明
print(zsh_in_jupyter.__doc__)


# In[6]:


zsh_in_jupyter.opendir()


# In[ ]:


get_ipython().system('open ')


# In[ ]:





# In[ ]:





# # Work with Files and Directories
# 似乎用的不太多，但还是写一点

# ## Create a File
# Command **touch** is used for creating a file. (md macos简直了，右键创建文件夹都得付费)

# In[19]:


get_ipython().system('touch test.sh')


# In[24]:


zsh_in_jupyter.opendir()


# ## Create a Directory

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




