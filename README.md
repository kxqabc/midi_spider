# midi_spider（MIDI文件爬虫程序）

作者：孔祥乾                    联系方式：15603072067                 邮箱：xiangqian_kong@126.com

---

> 简介：本程序主要用于自动爬取MIDI网站（"https://freemidi.org"）上所有的MIDI文件，并且获取MIDI文件对应的信息，保存在同级文件夹"info"下，信息文件的格式为JSON，文件名与对应的MIDI文件相同。

### 1. 运行依赖

- linux操作系统
- python2.7
- scrapy（python第三方库）

### 2. 使用方法

首先需要满足"1"中所有的运行依赖，将该项目代码文件夹"midi_spider"拷贝至任意目录，这里假设拷贝到："/home/midi_spider"，则在命令终端中输入：

```
cd /home/midi_spider		// 进入程序所在目录
scrapy crawl midi_spider	// 开始运行程序
```

**注意**：**该程序会依次遍历网站上所有的网页以获取所有MIDI文件及其信息，所以会持续运行2~3个小时，中途不得终止！**

### 3. 爬取结果与程序结构

在程序运行结束后，会在程序路径下会生成一个"midi"文件夹，这里面保存了从网站上爬取下来的所有MIDI文件及其信息文件，假设程序所在目录为"/home/midi_spider"，则文件目录树：

```
├── log.txt
├── midi_spider
│   ├── __init__.py
│   ├── items.py
│   ├── log.txt
│   ├── middlewares.py
│   ├── midi		// MIDI文件所在目录
│   │   ├── 0
│   │   ├── a
│   │   ├── b
│   │   ├── c
│   │   ├── d
│   │   ├── default
│   │   ├── e
│   │   ├── f
│   │   ├── g
│   │   ├── h
│   │   ├── i
│   │   ├── j
│   │   ├── k
│   │   ├── l
│   │   ├── m
│   │   ├── movie themes
│   │   ├── n
│   │   ├── o
│   │   ├── p
│   │   ├── q
│   │   ├── r
│   │   ├── s
│   │   ├── seasonal
│   │   ├── t
│   │   ├── u
│   │   ├── v
│   │   ├── video games
│   │   ├── w
│   │   ├── x
│   │   ├── y
│   │   └── z
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       ├── log.py
│       └── midi_spider.py
├── README.md
└── scrapy.cfg

```

如上所示，在目录"midi_spider/midi"下是爬取的所有的MIDI文件，所有的文件都已MIDI文件的文件名的首字母分别放在：0, a, b, c, ... , z文件夹下，而MIDI文件对应的信息（如：作者、风格、歌曲名等）都包含在该文件所在的路径下的"info"文件夹下，并且一个MIDI文件唯一对应一个信息文件（文件名相同，但信息文件为JSON格式）；

另外，由于该网站上的部分MIDI歌曲缺少"作者"、"风格"等信息，如电视、电影或游戏的BGM缺少作者信息，所以将其保存到对应的"movie themes"、"video games"文件夹下。