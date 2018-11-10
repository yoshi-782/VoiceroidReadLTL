import io, re, codecs, subprocess
from numpy.random import randint
from mastodon import Mastodon, StreamListener
from html.parser import HTMLParser

VRX_PATH = "VRX(民安☆Talkのパス)"
VOICEROID2_PATH = "VOICEROID2のパス"

#読み上げたいトゥートの文字列
readWords = [""]
#以下を含むトゥートは除外
filterWords = [""]
#除外したいユーザーID
filterID = [""]

#VOICEROID2のコマンド
voiceroid_command = {
    "c)":"結月ゆかり＞",
    "p)":"琴葉 茜＞",
    "u)":"琴葉 葵＞",
    "n)":"紲星あかり＞",
    "f)":"桜乃そら＞",
    "x)":"東北きりたん(v1)＞",
    "s)":"京町セイカ(v1)＞",
    "e)":"民安ともえ(v1)＞",
    "z)":"東北ずん子(v1)＞",
    "cj)":"結月ゆかり 喜び＞",
    "ci)":"結月ゆかり 怒り＞",
    "ck)":"結月ゆかり 悲しみ＞",
    "uj)":"琴葉 葵 喜び＞",
    "ui)":"琴葉 葵 怒り＞",
    "uk)":"琴葉 葵 悲しみ＞",
    "pj)":"琴葉 茜 喜び＞",
    "pi)":"琴葉 茜 怒り＞",
    "pk)":"琴葉 茜 悲しみ＞",
    "i)":"東北イタコ＞",
    "ia)":"東北イタコ あたふた＞",
    "ip)":"東北イタコ パワフル＞",
    "is)":"東北イタコ セクシー＞"
}

def main():
    try:
        mastodon = app()
        prosessCheck()

        print("読み上げを開始します。")
        mastodon.stream_local(Listener(readWords, filterWords, filterID), run_async=False)
    except KeyboardInterrupt:
        print("読み上げを終了します。")

def app():
    mastodon = Mastodon(
        client_id = "nico_app_clientcred.txt",
        access_token = "nico_usercred_Mastopy.txt",
        api_base_url = "https://friends.nico"
    )
    return mastodon

def prosessCheck() -> bool:
    proc = subprocess.Popen("tasklist", shell=True, stdout=subprocess.PIPE)
    a, b = True, True
    for line in proc.stdout:
        if str(line).count("vrx.exe") > 0 and a:
            a = False
        if str(line).count("VoiceroidEditor.exe") > 0 and b:
            b = False
    if a:
        print("vrx.exeが起動していないので起動させます。")
        subprocess.Popen(VRX_PATH.strip().split(" "))
    else:
        print("vrx.exeは起動しています。")
    if b:
        print("VOICEROIDが起動していないので起動させます。")
        subprocess.Popen(VOICEROID2_PATH.strip().split(" "))
    else:
        print("VOICEROIDは起動しています。")

class MyHtmlStripper(HTMLParser):
    def __init__(self, s):
        super().__init__()
        self.sio = io.StringIO()
        self.feed(s)

    def handle_data(self, data):
        self.sio.write(data)

    @property
    def value(self):
        return self.sio.getvalue()

class Listener(StreamListener):
    def __init__(self, readWords, filterWords, filterID, MAXLENGTH = 50):
        self.readWords = readWords
        self.filterWords = filterWords
        self.filterID = filterID
        self.MAXLENGTH = MAXLENGTH
        self.PURISET = list(voiceroid_command.values())

    def on_update(self, status):
        self.content = MyHtmlStripper(status['content']).value
        self.userName = status['account']['username']
        if self.__isRead(self.content):
            return

        self.content = self.__removalWords(self.content)
        self.content = self.__omissionWords(self.content)
        self.displayName = status['account']['display_name']
        self.yomiage()

    def yomiage(self):
        content = self.__replaceCommand()
        self.cmdLine(content)

    def __replaceCommand(self):
        b = False
        for t in voiceroid_command.keys():
            if self.content[:len(t)] == t:
                self.content = f"{voiceroid_command[t]}{self.displayName} {self.content[len(t):]}"
                b = True
            if self.content in f"\n{t}":
                self.content = self.content.replace(t, "\n" + voiceroid_command[t])
        if b == False:
            self.content = f"{self.PURISET[randint(len(self.PURISET))]}{self.displayName} {self.content}"

        return self.content

    def __isRead(self, content) -> bool: 
        for flt in self.filterWords:
            if self.content.find(flt) > -1:
                return True

        for id in self.filterID:
            if self.userName == id:
                return True
        
        for r in self.readWords:
            if self.content.find(r) > -1:
                return False
        
        #readもfilterもないので読まない
        return True

    def __omissionWords(self, content) -> str: 
        if len(content) >= self.MAXLENGTH:
            return content[:self.MAXLENGTH] + " 以下略"
        else:
            return content

    def __removalWords(self, contet):
        """URLが含まれていた場合、URL省略と置換＆カスタム絵文字を除去します"""
        contet = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "URL省略",contet)
        contet = re.sub(r":[@a-z]*?:", "", contet)
        return contet

    def cmdLine(self, cmd: str):
        subprocess.call(f"{VRX_PATH} {cmd}")
        print(self.format_text_write(cmd))

    def format_text_write(self, content):
        return content.encode('cp932', "ignore").decode('cp932')

if __name__ == "__main__": main()
