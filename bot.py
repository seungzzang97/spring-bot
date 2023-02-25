import discord, asyncio
import os

token = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.members = True
intents.message_content = True

### 채널 게시글 파일 불러오기
files = {
    "A.txt" : None, # 학원팟 신청 양식
    "AA.txt" : None, # 레이드 양식
    "B.txt" : None, # 규칙
    "C.txt" : None, # 공지사항
    "D.txt" : None, # 환영메시지
    "Messages.txt" : None, # 공용텍스트
}

for filename in files:
    with open(filename, "r", encoding="utf-8") as f:
        files[filename] = f.read()

A_TEXT = files["A.txt"]
AA_TEXT = files["AA.txt"] 
B_TEXT = files["B.txt"] 
C_TEXT = files["C.txt"]
D_TEXT = files["D.txt"]
MESSAGES = files["Messages.txt"]
### 채널 게시글 파일 불러오기

@client.event
async def on_ready():
    print("Running")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Lost Ark"))

@client.event
async def on_message(message):
    
    if message.author == client.user: # 봇 자신일 경우 아무 동작하지 않음
        return
    
    ### 채널 봇 게시글 등록
    if message.content == "!push" and message.author.id == 787605380209311744: # message.author.id는 정수 형태의 값으로 비교
        await message.delete()
        await message.channel.send(D_TEXT)
    ### 채널 봇 게시글 등록
              
    await form(message, 1077595514213781516, "!학원신청", A_TEXT, "!학원신청 명령어는 학원신청 채널에서 사용 하실 수 있습니다.")


### 채팅방 환영 메시지 
@client.event 
async def on_member_join(member):
    channel = client.get_channel(1077903295315714048)
    message = f"{member.mention}" + D_TEXT
    await channel.send(message)
### 채팅방 환영 메시지

### 양식 DM 전송 함수 ### await form(message, 채널, "명령어", 불러올파일, "명령어를 다른 채널에서 입력 했을 때 보낼 메시지")
async def form(message, f_id, f_command, content, content_2):
    if message.channel.id == f_id: # 채널 확인
        if message.content == f_command: # 입력 명령어 확인 // 개인 DM 전송
            if not message.author.dm_channel: # DM 채널 비활성화 됐을 경우
                dm_channel = await message.author.create_dm()
            else: # DM 채널 활성화 됐을 경우
                dm_channel = message.author.create_dm()
            await message.delete() # 작성한 메시지 삭제
            await message.author.dm_channel.send(content)

        else:
            await message.delete()
                
    elif message.channel.id != f_id and message.content == f_command: # 학원신청 채널이 아닌 채널에서 !양식 을 입력 했을 경우
        bot_message = await message.channel.send(content_2) 
        await asyncio.sleep(5)
        await bot_message.delete()
        await message.delete()
### 양식 DM 전송 함수 ###

    
        
client.run(token)


## await message.author.dm_channel.send() 후 봇이 개인 DM을 보내면서 새로운 messages 함수를 호출 해서 버그가 있었음 봇 자신일 경우 아무 것도 하지 않는 코드로 해결