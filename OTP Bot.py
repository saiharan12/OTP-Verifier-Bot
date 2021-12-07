import os
import csv

import time
import discord
from discord import member
from discord.guild import Guild
from dotenv import load_dotenv

otpcsv=open("otps.csv","r+")
otpfile=csv.reader(otpcsv,delimiter=",")
otplist=[]
for rows in otpfile:
    otplist.append(rows)
otpcsv.close()

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def branchfunc(a):
    bcode=a[0:2]
    if bcode=="AE":
        return "Aerospace"
    elif bcode=="CS":
        return "Comp-Sci"
    elif bcode=="EE":
        return "Electrical"
    elif bcode=="EP":
        return "Eng-Physics"
    elif bcode=="ME":
        return "Mechanical"
    elif bcode=="NA":
        return "Naval"
    elif bcode=="CH":
        return "Chemical"
    elif bcode=="BE":
        return "Bio-Eng"
    elif bcode=="ED":
        return "Eng-Design"
    elif bcode=="CE":
        return "Civil"
    elif bcode=="MM":
        return "Metallurgy"
    elif bcode=="BS":
        return "Bio-Sci"
    elif bcode=="PH":
        return "Phys"
    elif bcode=="HS":
        return "HSS"


def branchsuf(x):
    y=x[0:2]
    if y=="AE":
        return "Aero"
    elif y=="CS":
        return "CS"
    elif y=="EE":
        return "EE"
    elif y=="EP":
        return "EP"
    elif y=="ME":
        return "Mech"
    elif y=="NA":
        return "Naval"
    elif y=="CH":
        return "Chem"
    elif y=="BE":
        return "Bio En"
    elif y=="ED":
        return "ED"
    elif y=="CE":
        return "Civil"
    elif y=="MM":
        return "Meta"
    elif y=="BS":
        return "Bio Sci"
    elif y=="PH":
        return "Phy"
    elif y=="HS":
        return "HSS"



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    otpmsg=message.content
    msgsender=message.author


    try:
        rollnum,otpnum,servname=otpmsg.split(",")
        print(rollnum,otpnum,servname)

        for rowval in otplist:
            if rowval[0] == rollnum:
                if rowval[2]=='0':
                    if otpnum == rowval[1]:
                        
                        await message.channel.send("User Verified")

                        k=otplist.index(rowval)
                        otplist[k][2]=1

                        with open("otps.csv", 'w') as csvfile: 
                            csvwriter = csv.writer(csvfile,lineterminator = '\n')
                            csvwriter.writerows(otplist)                

                        

                        br=branchfunc(rollnum)
                        nroll=discord.utils.get(message.guild.roles, name=br)
                        vroll=discord.utils.get(message.guild.roles, name="Verified")
                        await msgsender.add_roles(nroll,vroll)


                        brs=branchsuf(rollnum)
                        nn = servname + " | " + brs
                        
                        await msgsender.edit(nick=nn)

                        time.sleep(0.1)
                        return
                    else:
                        await message.channel.send("Wrong OTP")
                        return
                else:
                    await message.channel.send("User Already Verified")
                    return
        else:
            await message.channel.send("Roll number not found")




        

    except:
        await message.channel.send("Wrong message format")





client.run(TOKEN)