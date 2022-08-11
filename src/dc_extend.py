import discord
from datetime import datetime
import json
import uuid
import random
from typing import Tuple


class FishingView(discord.ui.View):
    def __init__(self, author_id: int, cards: dict, fishing_img_url: str):
        super().__init__(timeout=60)
        self.__author_id = author_id
        self.__cards = cards
        self.__fishing_img_url = fishing_img_url

    # __init__()

    async def on_timeout(self):
        self.disable_view()

    # on_timeout()

    async def __get_embed(self, position: str) -> discord.Embed:
        """Get divination card (embed message)"""

        card = self.__cards.get(position)

        t_embed = discord.Embed(
            title="釣魚占卜", color=discord.Colour.from_rgb(222, 199, 241)
        )
        t_embed.set_author(
            name="EB Extend BOT",
            url="https://twitter.com/0xmimiQ",
            icon_url="https://i.imgur.com/DmV9HWw.png",
        )

        lucky_degree = card.get("LUCKY")
        lucky_status = ""

        if lucky_degree < 5:
            lucky_status = "⭐" * lucky_degree
        elif lucky_degree == 5:
            lucky_status = "🌸"
        elif lucky_degree > 5 and lucky_degree < 10:
            lucky_status = "🌸" + ("🍃" * (lucky_degree - 5))
        elif lucky_degree == 10:
            lucky_status = "👑"

        t_embed.add_field(name="🪶 ID", value=card.get("ID"), inline=True)
        t_embed.add_field(name="🎭 名稱", value=card.get("NAME"), inline=True)
        t_embed.add_field(
            name="🍀 幸運值", value=f"({lucky_degree}) {lucky_status}", inline=True
        )
        t_embed.add_field(name="🖊️ 解析", value=card.get("DESCRIPTION"), inline=False)
        t_embed.timestamp = datetime.now()
        t_embed.set_footer(text="占卜時間")
        t_embed.set_thumbnail(url=self.__fishing_img_url)

        return t_embed

    # __get_embed()

    def disable_view(self):
        for child in self.children:
            child.disabled = True

    # disable_view()

    @discord.ui.button(label="東海灣", emoji="⚓", style=discord.ButtonStyle.grey)
    async def button_0_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(
            view=self, embed=await self.__get_embed("EAST")
        )

    # button_0_callback()

    @discord.ui.button(label="南島", emoji="⛰", style=discord.ButtonStyle.grey)
    async def button_1_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(
            view=self, embed=await self.__get_embed("SOUTH")
        )

    # button_1_callback()

    @discord.ui.button(label="西之大漠", emoji="🏜", style=discord.ButtonStyle.grey)
    async def button_2_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(
            view=self, embed=await self.__get_embed("WEST")
        )

    # button_2_callback()

    @discord.ui.button(label="北之森", emoji="🌳", style=discord.ButtonStyle.grey)
    async def button_3_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(
            view=self, embed=await self.__get_embed("NORTH")
        )

    # button_3_callback()

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.__author_id


# class FishingView


class FishingWishForm(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="請填寫<物種名稱>"))
        self.add_item(
            discord.ui.InputText(label="請填寫<解析>", style=discord.InputTextStyle.long)
        )

    # __init__()

    async def callback(self, interaction: discord.Interaction):
        embed = None

        if not self.__success_goto_process():
            embed = discord.Embed(
                description="您的許願卡不幸被海怪吞了..下次再來吧!",
                color=discord.Colour.from_rgb(0, 255, 255),
            )
        # if
        else:
            seq = uuid.uuid4()
            (success, reason) = self.__make_wishing_card(seq)

            if not success:
                embed = discord.Embed(
                    description=reason, color=discord.Colour.from_rgb(0, 255, 255)
                )
            # if
            else:

                embed = discord.Embed(
                    description="您的許願卡已投入河中..",
                    color=discord.Colour.from_rgb(0, 255, 255),
                )
                embed.set_author(
                    name="EB Extend BOT",
                    url="https://twitter.com/0xmimiQ",
                    icon_url="https://i.imgur.com/DmV9HWw.png",
                )

                embed.add_field(name="🆕 許願序號", value=seq, inline=False)
                embed.add_field(
                    name="🎭 物種名稱", value=self.children[0].value, inline=False
                )
                embed.add_field(
                    name="🖊️ 解析", value=self.children[1].value, inline=False
                )
            # else
        # else

        embed.timestamp = datetime.now()
        embed.set_footer(text="Ebisu's Extend Bot")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # callback()

    def __success_goto_process(self) -> bool:
        """There's a certain chance that wishing function will fail."""
        base = random.randrange(1, 10)
        return base != random.randrange(1, 10)

    # __success_in_process

    def __make_wishing_card(self, seq: "uuid") -> Tuple[bool, str]:
        """
        Write wish card in json type.\n
        return ( success, reason )
        """

        card = {"NAME": self.children[0].value, "DESCRIPTION": self.children[1].value}

        try:
            file_name = f"wishing_card/{seq}.json"

            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(card, f, ensure_ascii=False, indent=4)

            return (True, "")
        # try

        except Exception as e:
            return (False, f"您的許願卡被無情的BUG怪獸吃了..下次再來吧!: {e}")

    # make_wishing_card


# class FishingWishForm


class TrackerMsgView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # __init__()


# TrackerMsgView
