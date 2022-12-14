import wenxin_api
from .text_to_image import TextToImage
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, Bot, MessageSegment
from nonebot.params import CommandArg
from utils.message_builder import image
from services.log import logger
from utils.message_builder import custom_forward_msg
from configs.config import Config
from typing import Type

__zx_plugin_name__ = "以文生图"
__plugin_usage__ = """
usage：
    用图片描述+图片风格生成图片
    指令：
        以文生图 图片风格 图片尺寸(非必填，默认方图) 图片描述
        
图片描述请不要带空格！      
风格可以是：油画、水彩、二次元、粉笔画、儿童画、蜡笔画、古风、像素风格、蒸汽波艺术、赛博朋克、概念艺术、未来主义、写实风格、超现实主义
尺寸可以是：方图(默认)、长图、横图
""".strip()
__plugin_des__ = "用图片风格+图片描述生成图片"
__plugin_cmd__ = ["以文生图/生成图片"]
__plugin_version__ = 1.2
__plugin_author__ = "CCYellowStar"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["以文生图", "生成图片"],
}
__plugin_configs__ = {
    "To_pic_ak": {
        "value": None,
        "help": "以文生图的ak_api,在https://wenxin.baidu.com/moduleApi/key 获取生成",
    },
    "To_pic_sk": {
        "value": None,
        "help": "以文生图的sk_api,在https://wenxin.baidu.com/moduleApi/key 获取生成",
    },
}

pic = on_command("以文生图", aliases={"生成图片"}, priority=5, block=True)
wenxin_api.ak = Config.get_config("zhenxun_plugin_TextToPic", "To_pic_ak")
wenxin_api.sk = Config.get_config("zhenxun_plugin_TextToPic", "To_pic_sk")



@pic.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, msg: Message = CommandArg()):
    msg = msg.extract_plain_text().strip().split()
    if not wenxin_api.ak:
        await pic.finish("以文生图的ak_api缺失，在https://wenxin.baidu.com/moduleApi/key 获取生成")
    if not wenxin_api.sk:
        await pic.finish("以文生图的sk_api缺失，在https://wenxin.baidu.com/moduleApi/key 获取生成")
    if len(msg) < 2:
        await pic.finish("请输入正确的格式：以文生图 图片风格 图片尺寸(非必填，可以是方图，长图，横图) 图片描述\n风格可以是：油画、水彩、卡通、粉笔画、儿童画、蜡笔画")
    if len(msg) == 3:
        text = msg[2]
        style = msg[0]
        if msg[1] =="方图":           
            resolution = "1024*1024"
        elif msg[1] =="长图":           
            resolution = "1024*1536"
        elif msg[1] =="横图":           
            resolution = "1536*1024"
        else:
            await pic.finish("请输入正确的尺寸：如方图、长图、横图，或者图片描述请不要带空格！")
    elif len(msg) == 2:
        text = msg[1]
        style = msg[0]
        resolution = "1024*1024"
    elif len(msg) > 3:
        await pic.finish("图片描述请不要带空格！")
    await get_img(text, style, resolution, pic, bot, event)


async def get_img(
text: str, style: str,resolution: str, matcher: Type[Matcher], bot: Bot, event: MessageEvent
):
    input_dict = {
    "text": text,
    "style": style,
    "resolution": resolution
    }
    try:
        await matcher.send("开始生成图片...")
        rst = await TextToImage.create(**input_dict)
        if isinstance(event, GroupMessageEvent):
            mes_list = []
            for i in rst["imgUrls"]:
                mes_list.append(image(i))
            mes_list = custom_forward_msg(mes_list, bot.self_id)
            await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)         
        else:
            for i in rst["imgUrls"]:
                await matcher.send(image(i))
    except Exception as e:
        await matcher.send(f"出错了！{type(e)}：{e}")
